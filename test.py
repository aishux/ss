import os
import pandas as pd
import re
import json
from bs4 import BeautifulSoup
from langchain_openai import AzureChatOpenAI
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from datetime import datetime
from sqlalchemy.engine import create_engine

# Azure Key Vault Configuration
KEY_VAULT_NAME = "your-key-vault-name"
SECRET_NAME = "AZURE-OPENAI-KEY"

credential = DefaultAzureCredential()
key_vault_url = f"https://{KEY_VAULT_NAME}.vault.azure.net"
client = SecretClient(vault_url=key_vault_url, credential=credential)
AZURE_OPENAI_KEY = client.get_secret(SECRET_NAME).value

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT = "your-openai-endpoint"
AZURE_DEPLOYMENT_NAME = "your-deployment-name"

llm = AzureChatOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    openai_api_key=AZURE_OPENAI_KEY,
    deployment_name=AZURE_DEPLOYMENT_NAME
)

# Databricks Connection Setup
DATABRICKS_SERVER = "your-databricks-server"
DATABRICKS_HTTP_PATH = "your-databricks-http-path"
DATABRICKS_TOKEN = "your-databricks-token"

engine = create_engine(
    f"databricks://token:{DATABRICKS_TOKEN}@{DATABRICKS_SERVER}:443/{DATABRICKS_HTTP_PATH}"
)

def clean_html(comment):
    """Removes HTML tags, special characters, and ensures proper formatting."""
    text = BeautifulSoup(str(comment), "html.parser").get_text()
    text = re.sub(r"[^a-zA-Z0-9\s+-]", "", text)  # Remove special characters except + and -
    text = re.sub(r"\s+", " ", text).strip()  # Normalize spaces
    text = re.sub(r"(\b\w+\b) \1", r"\1", text)  # Remove duplicate words
    return text

def get_user_filters():
    """Prompts user for filter inputs and returns a dictionary of filters."""
    filter_columns = ["ACCOUNT_ID", "FUNCTION_ID", "REPORT_ID", "PERIOD", "LEAF_FUNC_DESC"]
    filters = {}
    
    for column in filter_columns:
        value = input(f"Enter {column} (leave blank to skip): ").strip()
        if value:
            filters[column] = value
    
    return filters if filters else None

def fetch_and_clean_data(filters=None):
    """Fetches commentary data from Databricks, applies filters, and cleans HTML comments."""
    if filters:
        query = "SELECT * FROM PROVISION.CC_COMMENTARY_CUBE2_VW WHERE " + " AND ".join(
            [f"{key} = '{value}'" for key, value in filters.items()]
        )
    else:
        query = """
        SELECT ACCOUNT_ID, ACCOUNT_DESC, FUNCTION_ID, FUNCTION_DESC, REPORT_ID, PERIOD, 
               REPORTING_DATE, REPORTING_VIEW, LEAF_FUNC_DESC, COMMENT, CREATED_BY, CREATED_ON
        FROM PROVISION.CC_COMMENTARY_CUBE2_VW
        """
    
    df = pd.read_sql(query, engine)
    df["COMMENT"] = df["COMMENT"].apply(clean_html)
    return df

def summarize_comments(df):
    """Summarizes comments based on LEAF_FUNC_DESC in a single paragraph format."""
    grouped_comments = df.groupby("LEAF_FUNC_DESC")["COMMENT"].apply(lambda x: ". ".join(x)).reset_index()
    
    summaries = []
    for _, row in grouped_comments.iterrows():
        # Sample input and output to guide the model
        sample_input = (
            "The sales increased by 10% due to higher demand in the region. "
            "The marketing campaign was successful, leading to a 15% increase in customer engagement. "
            "However, supply chain issues caused a delay in product delivery."
        )
        sample_output = (
            "The sales growth of 10% was driven by increased regional demand and a successful marketing campaign, "
            "which boosted customer engagement by 15%. However, supply chain disruptions led to delays in product delivery."
        )
        
        summary_prompt = (
            f"Summarize the following comments related to {row['LEAF_FUNC_DESC']}. "
            "Capture key insights, main drivers, and significant impacts. Ensure clarity and remove "
            "redundancy while preserving essential details. Provide the summary in paragraph format. "
            "Here is a sample input and output for reference:\n\n"
            f"Sample Input: {sample_input}\n\n"
            f"Sample Output: {sample_output}\n\n"
            f"Now, summarize the following comments:\n{row['COMMENT']}"
        )
        
        response = llm.invoke(summary_prompt)
        summary_content = response.content if hasattr(response, "content") else str(response)
        summaries.append(f"{row['LEAF_FUNC_DESC']}: {summary_content}")
    
    summary_text = " ".join(summaries)
    return pd.DataFrame([{ "LEAF_FUNC_DESC": "Summary", "COMMENT": summary_text }])

def save_to_csv(df):
    """Saves the DataFrame to a CSV file in the output_files folder with an incremental filename."""
    output_dir = "output_files"
    os.makedirs(output_dir, exist_ok=True)
    
    file_number = 1
    while os.path.exists(os.path.join(output_dir, f"cleaned_commentary{file_number}.csv")):
        file_number += 1
    
    file_path = os.path.join(output_dir, f"cleaned_commentary{file_number}.csv")
    df.to_csv(file_path, index=False)
    print(f"\nData saved to {file_path}")
    
def write_summary_to_databricks(summary_df):
    """Writes the summary row back to the Databricks table etl.frs_gf."""
    summary_df.to_sql("frs_gf", engine, schema="etl", if_exists="append", index=False)

def main():
    """Main function to fetch, clean data, summarize comments, and print results."""
    filters = get_user_filters()
    df = fetch_and_clean_data(filters)
    print("\nCleaned Data:")
    print(df.head())
    
    if not df.empty:
        summary_df = summarize_comments(df)
        summary_df["CREATED_BY"] = "AI_Generated"
        summary_df["CREATED_ON"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        df = pd.concat([df, summary_df], ignore_index=True)
        
        # Write summary row back to Databricks
        write_summary_to_databricks(summary_df)
    
    # Save to CSV
    df.to_csv("cleaned_commentary.csv", index=False)
    print("\nData saved to cleaned_commentary.csv")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
