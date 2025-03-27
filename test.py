import os
from databricks.connect import DatabricksSession
from pyspark.sql import SparkSession

# Set Databricks Connect configuration inline
os.environ["DATABRICKS_HOST"] = "https://dbc-xxxxxxxx.cloud.databricks.com"  # Replace with your Databricks workspace URL
os.environ["DATABRICKS_TOKEN"] = "your-access-token"  # Replace with your Databricks personal access token
os.environ["DATABRICKS_CLUSTER_ID"] = "your-cluster-id"  # Replace with your Databricks cluster ID
os.environ["DATABRICKS_HTTP_PATH"] = "/sql/1.0/warehouses/your-warehouse-id"  # (Optional) For Databricks SQL warehouses

# Initialize Databricks Connect session
spark = DatabricksSession.builder.getOrCreate()

# Sample DataFrame
data = [(1, "Alice", 25), (2, "Bob", 30), (3, "Charlie", 35)]
columns = ["id", "name", "age"]
df = spark.createDataFrame(data, columns)

# Define database and table name
database_name = "default"  # Change as needed
table_name = "users"
full_table_name = f"{database_name}.{table_name}"

# Write DataFrame to Databricks as a Delta table
df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable(full_table_name)

print(f"Table {full_table_name} saved successfully.")
