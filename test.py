import subprocess
import sys

def safe_run(command, description):
    try:
        print(f"\n🚀 Running: {description}")
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
    [sys.executable, "-m", "pip", "install", "databricks-connect==12.2.8"],
    "Installing databricks-connect"
)

# Step 2: Configure databricks-connect using Python module (instead of CLI executable)
safe_run(
    [
        sys.executable, "-m", "databricks_connect.cli", "configure", "--token",
        "--host", "https://<your-databricks-instance>",
        "--token-value", "<your-token>",
        "--cluster-id", "<your-cluster-id>",
        "--org-id", "<your-org-id>",
        "--port", "15001"
    ],
    "Configuring databricks-connect"
)

# Step 3: Continue with main application logic
print("\n🎯 Setup complete (or skipped due to error). Continuing with the application...")
# Your app logic starts here
