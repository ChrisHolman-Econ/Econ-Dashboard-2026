# Ingest Current Employment Statistics (CES) data from BLS API
import pandas as pd
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
BLS_KEY = os.getenv("BLS_KEY")
# Ensure BLS_KEY is set
def ingest_bls_data(series_ids, start_year, end_year):   
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    
    # Payload expects a LIST of IDs
    payload = {
        "seriesid": series_ids, 
        "startyear": str(start_year),
        "endyear": str(end_year),
        "registrationKey": BLS_KEY
    }
    
    response = requests.post(url, json=payload)
    data = response.json()
    
    # Logic to combine multiple series (Like ldply or map_dfr in R)
    all_series = []
    for s in data['Results']['series']:
        temp_df = pd.DataFrame(s['data'])
        temp_df['series_id'] = s['seriesID']
        all_series.append(temp_df)
    
    df = pd.concat(all_series)

    # Clean dates and handle the "-" character safely
    # 1. Create a cleaner string by adding spaces: "2025 Dec 1"
    date_strings = df['year'] + " " + df['periodName'].str[:3] + " 1"
    
    # 2. Tell pandas exactly how to read it: Year (%Y), Month Abbreviation (%b), Day (%d)
    df['date'] = pd.to_datetime(date_strings, format='%Y %b %d')
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    
    return df.dropna(subset=['value']).sort_values(['series_id', 'date'])
# --- Execution ---
if __name__ == "__main__":
    ids = ["CES0000000001"] # National total employment series ID
    
    try:
        df_labor = ingest_bls_data(ids, 2015, 2026)
        
        os.makedirs('data/raw', exist_ok=True)
        df_labor.to_csv("data/raw/bls_ces_raw.csv", index=False)
        print("✅ Success! Data for all 3 series saved.")
        print(df_labor.sample(5)) # Show a random sample of the data
        
    except Exception as e:
        print(f"❌ Error: {e}")
