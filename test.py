import requests
import time
import pandas as pd
from io import StringIO

API_BASE = "https://cirrsup-frs-talk2data-dev2-backend.azurewebsites.net"

def submit_job():
    """Submit a long job and get job_id"""
    url = f"{API_BASE}/summation/start?business_division=GF"
    response = requests.post(url)
    response.raise_for_status()
    return response.json()["job_id"]

def check_status(job_id):
    """Check if job is done"""
    url = f"{API_BASE}/summation/status/{job_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def fetch_result(job_id):
    """Fetch CSV result"""
    url = f"{API_BASE}/summation/result/{job_id}"
    response = requests.get(url)
    response.raise_for_status()
    return pd.read_csv(StringIO(response.text))

# ---- main flow ----
job_id = submit_job()
print(f"✅ Job submitted: {job_id}")

while True:
    status = check_status(job_id)
    print("⏳ Status:", status)

    if status["state"] == "completed":
        break
    elif status["state"] == "failed":
        raise RuntimeError("❌ Job failed!")

    time.sleep(15)  # poll every 15 seconds

df = fetch_result(job_id)
print("🎉 DataFrame loaded")
print(df.head())
