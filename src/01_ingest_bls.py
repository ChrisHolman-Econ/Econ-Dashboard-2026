# Ingest BLS CPI data from BLS API using bls_utils.py
from bls_utils import fetch_bls_data  # Import your custom "package"
import os

# Define what you want
CPI_IDS = ["CUUR0000SA0"]
START = 2015
END = 2026

# Run the machine
print("Pulling Consumer Price Index data...")
df = fetch_bls_data(CPI_IDS, START, END)

# Save the result
os.makedirs('data/raw', exist_ok=True)
df.to_csv("data/raw/bls_cpi_raw.csv", index=False)
print("✅ Done!")
