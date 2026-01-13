# Import Libraries
import pandas as pd
import numpy as np
import requests
from dotenv import load_dotenv
import os
from io import StringIO
load_dotenv()  # This line actually loads the variables from the .env file

# Call BLS Key from Environment Variable
BLS_KEY = os.getenv("BLS_KEY")
if BLS_KEY is None:
    raise ValueError("BLS_KEY environment variable not set.")

# Define Function to Ingest BLS Data
def ingest_bls_data(series_id, start_year, end_year):   
    # Define BLS API Endpoint and Headers
    bls_api_url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    headers = {'Content-Type': 'application/json'}
    
    # Prepare Payload for API Request
    payload = {
        "seriesid": [series_id],
        "startyear": str(start_year),
        "endyear": str(end_year),
        "registrationKey": BLS_KEY
    }
    
    # Make API Request
    response = requests.post(bls_api_url, json=payload, headers=headers)
    
    # Check for Successful Response
    if response.status_code != 200:
        raise Exception(f"Error fetching data from BLS API: {response.status_code}")
    
    # Parse JSON Response
    data = response.json()
    
    # Extract Time Series Data
    if 'Results' not in data or 'series' not in data['Results']:
        raise Exception("Invalid response structure from BLS API.")
    
    series_data = data['Results']['series'][0]['data']
    
    # Convert to DataFrame
    df = pd.DataFrame(series_data)
    
    # Convert Year and Period to Datetime
    df['date'] = pd.to_datetime(df['year'] + df['periodName'].str[:3] + ' 1', format='%Y%b %d')

# Convert Value to Numeric
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df = df.dropna(subset=['value'])
    
    # Sort and clean up
    df = df.sort_values('date').reset_index(drop=True)
    df = df[['date', 'value']]
    
    return df

# --- Execution ---
if __name__ == "__main__":
    # 1. Define the variables FIRST
    series_id = "CUUR0000SA0" 
    start_year = 2015
    end_year = 2026
    
    print(f"Fetching data for {series_id}...")
    
    # 2. Now pass them into the function
    try:
        df_inflation = ingest_bls_data(series_id, start_year, end_year)
        
        # 3. Success check
        print("\n--- Data Preview ---")
        print(df_inflation.tail()) 
        
        # 4. Save the file
        os.makedirs('data/raw', exist_ok=True)
        file_path = f"data/raw/bls_cpi_raw.csv"
        df_inflation.to_csv(file_path, index=False)
        print(f"\n✅ Success! Data saved to {file_path}")
        
    except Exception as e:
        print(f"❌ An error occurred: {e}")

# extract data
ingest_bls_data(series_id, start_year, end_year)
