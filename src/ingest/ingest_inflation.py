# Ingest BLS CPI data from BLS API using bls_utils.py
import sys
from pathlib import Path

# Go up one level (to src/) so Python can find bls_utils.py
src_path = Path(__file__).resolve().parent.parent
sys.path.append(str(src_path))

from bls_utils import fetch_bls_data  # Import your custom "package"
import os

# Define what you want
CPI_IDS = ["CUUR0000SA0", "CUUR0200SA0"]
START = 2015
END = 2026

# Run the machine
print("Pulling Consumer Price Index data...")
df = fetch_bls_data(CPI_IDS, START, END)

# Save the result
os.makedirs('data/raw', exist_ok=True)
df.to_csv("data/raw/inflation_raw.csv", index=False)
print("✅ Done!")
