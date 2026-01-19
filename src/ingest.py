import os
import bls_utils

# This file ingests multiple BLS data series using a modular approach
SERIES_IDS = {
    'CUUR0000SA0': 'US_Inflation',
    'CUUR0200SA0': 'MI_Inflation',
    'LNS14000000': 'US_Unemployment',
    'LASST260000000000003': 'MI_Unemployment',
    'CES0000000001': 'US_Employment',
    'SMS26000000000000001': 'MI_Employment'
}

def run_ingestion():
    print("🚀 Starting modular ingestion...")
    os.makedirs("data/raw", exist_ok=True)
    
    # Call the utility function
    data_bundles = bls_utils.fetch_bls_series(SERIES_IDS, 2016, 2026)
    
    # Save each one using the friendly name
    for name, df in data_bundles.items():
        file_path = f"data/raw/{name}_raw.csv"
        df.to_csv(file_path, index=False)
        print(f"✅ Saved: {file_path}")

if __name__ == "__main__":
    run_ingestion()