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


def fetch_data(filters: dict = None):
    """Fetches commentary data based on filters."""
    base_query = """
    SELECT ACCOUNT_ID, ACCOUNT_DESC, FUNCTION_ID, FUNCTION_DESC, REPORT_ID, PERIOD, 
           REPORTING_DATE, REPORTING_VIEW, COMMENT
    FROM PROVISION.CC_COMMENTARY_CUBE2_VW
    """
    
    # Apply filters if provided
    if filters:
        filter_conditions = " AND ".join([f"{k} = '{v}'" for k, v in filters.items()])
        base_query += f" WHERE {filter_conditions}"
    
    df = pd.read_sql(base_query, engine)
    return df


def clean_html(comment):
    """Removes HTML tags from comments."""
    return BeautifulSoup(comment, "html.parser").get_text()


def summarize_comments(df):
    """Summarizes comments using Azure OpenAI."""
    grouped = df.groupby([
        "ACCOUNT_ID", "ACCOUNT_DESC", "FUNCTION_ID", "FUNCTION_DESC", "REPORT_ID", "PERIOD", "REPORTING_DATE", "REPORTING_VIEW" 
    ])
    
    summarized_comments = []
    for group, data in grouped:
        cleaned_comments = " ".join([clean_html(comment) for comment in data["COMMENT"]])
        prompt = f"Summarize the following comments: {cleaned_comments}"
        summary = llm.complete(prompt)
        summarized_comments.append(list(group) + [summary])
    
    return pd.DataFrame(summarized_comments, columns=[
        "ACCOUNT_ID", "ACCOUNT_DESC", "FUNCTION_ID", "FUNCTION_DESC", "REPORT_ID", "PERIOD", "REPORTING_DATE", "REPORTING_VIEW", "SUMMARIZED_COMMENT"
    ])


def main():
    """Main function to execute summarization."""
    filters = {  # Example filters, modify as needed
        "ACCOUNT_ID": "U52100",
        "FUNCTION_ID": "N0000",
        "REPORT_ID": "GF_Estimate",
        "PERIOD": "all",
        "REPORTING_VIEW": "Integration"
    }
    df = fetch_data(filters)
    summarized_df = summarize_comments(df)
    print(summarized_df)
    print("Summarization complete.")


if __name__ == "__main__":
    main()
