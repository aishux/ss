import subprocess
import sys

def safe_run(command, description, input_text=None):
    try:
        print(f"\n🚀 Running: {description}")
        if input_text:
            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate(input=input_text)
            if process.returncode == 0:
                print(f"✅ Success: {description}")
            else:
                print(f"⚠️ Failed: {description}")
                print(stderr)
        else:
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

# Replace with your actual values or use environment variables for security

# When running first time
# inputs = """\
# y
# https://demo.cloud.databricks.com
# helloworld
# 112312
# 123123
# 15001
# """

# If already ran once:
inputs = """\
https://demo.cloud.databricks.com
hellu
112312
123123
15001
"""

print(sys.executable)

# Step 2: Configure databricks-connect using Python module
safe_run(
    [sys.executable, "-m", "pyspark.databricks_connect", "configure"],
    "Configuring databricks-connect",
    input_text=inputs
)

# Step 3: Continue with main application logic
print("\n🎯 Setup complete (or skipped due to error). Continuing with the application...")
# Your app logic starts here
