import os
import pandas as pd
import sqlalchemy
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


def fetch_and_clean_data():
    """Fetches entire commentary table and cleans HTML comments."""
    query = """
    SELECT ACCOUNT_ID, ACCOUNT_DESC, FUNCTION_ID, FUNCTION_DESC, REPORT_ID, PERIOD, 
           REPORTING_DATE, REPORTING_VIEW, COMMENT
    FROM PROVISION.CC_COMMENTARY_CUBE2_VW
    """
    
    df = pd.read_sql(query, engine)
    df["COMMENT"] = df["COMMENT"].apply(clean_html)
    return df, query


def main():
    """Main function to fetch and clean data."""
    df, query = fetch_and_clean_data()
    print("Generated SQL Query:")
    print(query)
    print("\nCleaned Data:")
    print(df.head())

    # Save to CSV
    df.to_csv("cleaned_commentary.csv", index=False)
    print("\nData saved to cleaned_commentary.csv")



if __name__ == "__main__":
    main()
