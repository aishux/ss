from dotenv import load_dotenv
import os

# Load the environment variables from local.env
load_dotenv("local.env")

# Build the multiline input string
inputs = "\n".join([
    os.getenv("confirm", "y"),
    os.getenv("databricks_hostname", ""),
    os.getenv("token", ""),
    os.getenv("cluster_id", ""),
    os.getenv("org_id", ""),
    os.getenv("port", ""),
]) + "\n"

# Now use `inputs` in your subprocess call
safe_run(
    [sys.executable, "-m", "pyspark.databricks_connect", "configure"],
    "Configuring databricks-connect",
    input_text=inputs
)
