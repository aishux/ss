import os
import pandas as pd
import sqlalchemy
import re
import json
from sqlalchemy.engine import create_engine
from openai import AzureOpenAI
from bs4 import BeautifulSoup

# Database Connection Setup
DATABRICKS_SERVER = "your-databricks-server"
DATABRICKS_HTTP_PATH = "your-databricks-http-path"
DATABRICKS_TOKEN = "your-databricks-token"

engine = create_engine(
    f"databricks://token:{DATABRICKS_TOKEN}@{DATABRICKS_SERVER}:443/{DATABRICKS_HTTP_PATH}"
)

# Azure OpenAI Configuration
AZURE_OPENAI_KEY = "your-api-key"
AZURE_OPENAI_ENDPOINT = "your-openai-endpoint"
AZURE_DEPLOYMENT_NAME = "your-deployment-name"

llm = AzureOpenAI(api_key=AZURE_OPENAI_KEY, endpoint=AZURE_OPENAI_ENDPOINT, deployment_name=AZURE_DEPLOYMENT_NAME)


def clean_html(comment):
    """Removes HTML tags, special characters, and ensures proper formatting."""
    text = BeautifulSoup(str(comment), "html.parser").get_text()
    text = re.sub(r"[^a-zA-Z0-9\s+-]", "", text)  # Remove special characters except + and -
    text = re.sub(r"\s+", " ", text).strip()  # Normalize spaces
    text = re.sub(r"(\b\w+\b) \1", r"\1", text)  # Remove duplicate words
    return text


def fetch_and_clean_data(filters=None):
    """Fetches commentary data, applies filters, and cleans HTML comments."""
    base_query = """
    SELECT ACCOUNT_ID, ACCOUNT_DESC, FUNCTION_ID, FUNCTION_DESC, REPORT_ID, PERIOD, 
           REPORTING_DATE, REPORTING_VIEW, COMMENT
    FROM PROVISION.CC_COMMENTARY_CUBE2_VW
    """
    
    if filters:
        filter_conditions = " AND ".join([f"{key} = '{value}'" for key, value in filters.items()])
        query = base_query + " WHERE " + filter_conditions
    else:
        query = base_query
    
    df = pd.read_sql(query, engine)
    df["COMMENT"] = df["COMMENT"].apply(clean_html)
    return df, query


def summarize_comments(df):
    """Summarizes comments for the retrieved dataset."""
    summary_prompt = "Summarize the following comments:\n" + "\n".join(df["COMMENT"].tolist())
    response = llm.chat_completions.create(
        model=AZURE_DEPLOYMENT_NAME,
        messages=[{"role": "user", "content": summary_prompt}],
        temperature=0.5
    )
    return response.choices[0].message.content.strip()


def main(filters=None):
    """Main function to fetch, clean data, summarize comments, and print results."""
    df, query = fetch_and_clean_data(filters)
    print("Generated SQL Query:")
    print(query)
    print("\nCleaned Data:")
    print(df.head())
    
    if not df.empty:
        summary = summarize_comments(df)
        summary_row = df.iloc[0].copy()
        summary_row["COMMENT"] = summary
        df = pd.concat([df, pd.DataFrame([summary_row])], ignore_index=True)
    
    # Save to CSV
    df.to_csv("cleaned_commentary.csv", index=False)
    print("\nData saved to cleaned_commentary.csv")


if __name__ == "__main__":
    user_filters = {"ACCOUNT_ID": "U52100", "FUNCTION_ID": "N0000"}  # Example filters
    main(filters=user_filters)
