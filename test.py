import pandas as pd
from sqlalchemy import create_engine

# Databricks connection details
DATABRICKS_HOST = "your-databricks-instance"  # Example: dbc-xxxxxxxx.cloud.databricks.com
DATABRICKS_TOKEN = "your-access-token"
DATABRICKS_HTTP_PATH = "your-http-path"
DATABASE_NAME = "default"
TABLE_NAME = "users"

# JDBC connection URL
jdbc_url = f"databricks+connector://token:{DATABRICKS_TOKEN}@{DATABRICKS_HOST}:443/{DATABASE_NAME}"

# Create SQLAlchemy engine
engine = create_engine(jdbc_url)

# Sample Pandas DataFrame
data = {"id": [1, 2, 3], "name": ["Alice", "Bob", "Charlie"], "age": [25, 30, 35]}
df = pd.DataFrame(data)

# Write DataFrame to Databricks table
df.to_sql(TABLE_NAME, con=engine, if_exists="replace", index=False)

print(f"Table {DATABASE_NAME}.{TABLE_NAME} saved successfully.")
