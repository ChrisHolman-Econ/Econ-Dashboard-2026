# Ingest economic data from BLS API using bls_utils.py
import pandas as pd
import requests
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("BLS_KEY")

# Series IDs directory mapping
SERIES_IDS = {
    'US_Inflation': 'CUUR0000SA0',    # US All Items Index (Level)
    'MI_Inflation': 'CUUR0200SA0',
    'US_Unemployment': 'LNS14000000',
    'MI_Unemployment': 'LASST260000000000003',
    'US_Employment': 'CES0000000001',
    'MI_Employment': 'SMS26000000000000001'
}

# Create look for extracting API data
for name, series_id in SERIES_IDS.items():
    print(f"--- Fetching data for: {name} ---")
    
    # We put the s_id into the request
    url = f"https://api.bls.gov/publicAPI/v2/timeseries/data/{series_id}?registrationkey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if data['status'] == 'REQUEST_SUCCEEDED':
        # Grab the list of data points
        results = data['Results']['series'][0]['data']
        df = pd.DataFrame(results)
        
        # Save to raw folder using the name from our dictionary
        file_path = f"data/raw/{name}_raw.csv"
        df.to_csv(file_path, index=False)
        print(f"Saved {len(df)} rows to {file_path}")
    else:
        print(f"Failed to get {name}: {data['message']}")
    
    print(f"Success! Saved as data/raw/{name}_raw.csv")