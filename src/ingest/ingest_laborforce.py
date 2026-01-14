# Ingest Labor Force Data from BLS API using bls_utils.py
from bls_utils import fetch_bls_data  # Import your custom "package"
import os

# Define what you want
LABOR_IDS = ["LNS11000000", "LNS13000000", "LNS14000000"]
START = 2015
END = 2026

# Run the machine
print("Pulling Labor Force data...")
df = fetch_bls_data(LABOR_IDS, START, END)

# Save the result
os.makedirs('data/raw', exist_ok=True)
df.to_csv("data/raw/bls_laborforce_raw.csv", index=False)
print("✅ Done!")