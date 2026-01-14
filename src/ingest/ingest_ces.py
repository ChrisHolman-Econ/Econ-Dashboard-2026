# Ingest Current Employment Statistics (CES) data from BLS API
import sys
from pathlib import Path

# Go up one level (to src/) so Python can find bls_utils.py
src_path = Path(__file__).resolve().parent.parent
sys.path.append(str(src_path))

from bls_utils import fetch_bls_data  # Import your custom "package"
import os

# Define what you want
CES_IDS = ["CES0000000001"]
START = 2015
END = 2026

# Run the machine
print("Pulling Current Employment Statistics data...")
df = fetch_bls_data(CES_IDS, START, END)

# Save the result
os.makedirs('data/raw', exist_ok=True)
df.to_csv("data/raw/bls_ces_raw.csv", index=False)
print("✅ Done!")
