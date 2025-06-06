import subprocess

def safe_run(command, description):
    try:
        print(f"Running: {description}")
        subprocess.run(command, check=True)
        print(f"✅ Success: {description}")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Failed: {description}")
        print(f"Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error during: {description}")
        print(f"Error: {e}")

# Step 1: Install databricks-connect
safe_run(
    ["pip", "install", "databricks-connect==12.2.8"],
    "Installing databricks-connect"
)

# Step 2: Configure databricks-connect
safe_run(
    [
        "databricks-connect", "configure", "--token",
        "--host", "https://<your-databricks-instance>",
        "--token-value", "<your-token>",
        "--cluster-id", "<your-cluster-id>",
        "--org-id", "<your-org-id>",
        "--port", "15001"
    ],
    "Configuring databricks-connect"
)

# Proceed with your application logic here
print("🎯 Continuing with the main application...")
