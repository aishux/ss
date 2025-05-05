import os
import pandas as pd
import re
from bs4 import BeautifulSoup
from datetime import datetime
from sqlalchemy.engine import create_engine
from langchain_openai import AzureChatOpenAI
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Load prompt templates and config as Python modules
import prompts
import config

PROMPTS = prompts.PROMPTS
CONFIG = config.CONFIG

class SummationAgent:
    def __init__(self, key_vault_name, secret_name, openai_endpoint, deployment_name,
                 databricks_server, databricks_http_path, databricks_token, business_division):
        self.key_vault_name = key_vault_name
        self.secret_name = secret_name
        self.openai_endpoint = openai_endpoint
        self.deployment_name = deployment_name
        self.databricks_server = databricks_server
        self.databricks_http_path = databricks_http_path
        self.databricks_token = databricks_token
        self.business_division = business_division

        self.config = CONFIG[business_division]
        self.table_name = self.config["table_name"]
        self.columns = self.config["columns"]

        self.openai_key = self.get_openai_key()
        self.llm = self.initialize_llm()
        self.engine = self.initialize_engine()

    def get_openai_key(self):
        credential = DefaultAzureCredential()
        key_vault_url = f"https://{self.key_vault_name}.vault.azure.net"
        client = SecretClient(vault_url=key_vault_url, credential=credential)
        return client.get_secret(self.secret_name).value

    def initialize_llm(self):
        return AzureChatOpenAI(
            azure_endpoint=self.openai_endpoint,
            openai_api_key=self.openai_key,
            deployment_name=self.deployment_name
        )

    def initialize_engine(self):
        return create_engine(
            f"databricks://token:{self.databricks_token}@{self.databricks_server}:443/{self.databricks_http_path}"
        )

    def clean_html(self, comment):
        text = BeautifulSoup(str(comment), "html.parser").get_text()
        text = re.sub(r"[^a-zA-Z0-9\s+-]", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        text = re.sub(r"(\b\w+\b) \1", r"\1", text)
        return text

    def fetch_and_clean_data(self):
        column_str = ", ".join(self.columns)
        query = f"SELECT {column_str} FROM {self.table_name}"
        df = pd.read_sql(query, self.engine)

        if not df.empty and 'BUSINESS_DIVISION' in df.columns and 'GF' in df['BUSINESS_DIVISION'].unique():
            df.loc[df['BUSINESS_DIVISION'] == 'GF', 'COMMENT'] = df['COMMENT'].apply(self.clean_html)

        return df

    def summarize_comments(self, df):
        summaries = []

        for aggregation_set, group in df.groupby("AGGREGATION_SET"):
            grouped_comments = group.groupby("LEAF_FUNC_DESC")["COMMENT"].apply(lambda x: ". ".join(x)).reset_index()

            summary_texts = []
            prompt_template = PROMPTS.get(self.business_division, PROMPTS["DEFAULT"])['prompt']

            for _, row in grouped_comments.iterrows():
                summary_prompt = prompt_template.format(leaf_func=row['LEAF_FUNC_DESC'], comments=row['COMMENT'])
                response = self.llm.invoke(summary_prompt)
                summary_content = response.content if hasattr(response, "content") else str(response)
                summary_texts.append(f"{row['LEAF_FUNC_DESC']}: {summary_content}")

            summary_text = " ".join(summary_texts)
            base_row = group.iloc[0].to_dict()
            base_row.update({
                "LEAF_FUNC_DESC": "Summary",
                "COMMENT": summary_text,
                "CREATED_BY": "AI_Generated",
                "CREATED_ON": datetime.now().strftime("%d/%m/%Y %H:%M")
            })
            summaries.append(base_row)

        return pd.DataFrame(summaries)

    def write_summary_to_databricks(self, summary_df):
        output_table = PROMPTS.get(self.business_division, PROMPTS["DEFAULT"]).get("output_table", "etl.frs_default")
        schema_name, table_name = output_table.split(".")
        summary_df.to_sql(table_name, self.engine, schema=schema_name, if_exists="append", index=False)

    def save_to_csv(self, df, filename="cleaned_commentary.csv"):
        df.to_csv(filename, index=False)

    def run(self):
        df = self.fetch_and_clean_data()
        print("\nCleaned Data:")
        print(df.head())

        if not df.empty:
            summary_df = self.summarize_comments(df)
            self.write_summary_to_databricks(summary_df)
            self.save_to_csv(df)
            print("\nData saved to cleaned_commentary.csv")

if __name__ == "__main__":
    summarizer = SummationAgent(
        key_vault_name="your-key-vault-name",
        secret_name="AZURE-OPENAI-KEY",
        openai_endpoint="your-openai-endpoint",
        deployment_name="your-deployment-name",
        databricks_server="your-databricks-server",
        databricks_http_path="your-databricks-http-path",
        databricks_token="your-databricks-token",
        business_division="GF"
    )
    summarizer.run()
