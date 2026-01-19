import pandas as pd
import requests
import os
from dotenv import load_dotenv
from pathlib import Path

base_dir = Path(__file__).resolve().parent
load_dotenv(base_dir / ".env")

BLS_KEY = os.getenv("BLS_KEY")

def fetch_bls_series(series_map, start_year, end_year):
    """
    Fetches multiple series and returns a dictionary of DataFrames 
    mapped to your custom names.
    """
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    payload = {
        "seriesid": list(series_map.keys()),
        "startyear": str(start_year),
        "endyear": str(end_year),
        "registrationKey": BLS_KEY
    }
    
    response = requests.post(url, json=payload)
    data = response.json()
    
    if data['status'] != 'REQUEST_SUCCEEDED':
        raise ValueError(f"BLS API Error: {data.get('message')}")

    results_dict = {}
    for s in data['Results']['series']:
        s_id = s['seriesID']
        friendly_name = series_map[s_id] # Look up the name (e.g., 'US_Inflation')
        
        df = pd.DataFrame(s['data'])
        
        # Clean the dates immediately
        date_series = df['year'] + " " + df['periodName'].str[:3] + " 1"
        df['date'] = pd.to_datetime(date_series, format='%Y %b %d')
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        
        results_dict[friendly_name] = df.sort_values('date')
        
    return results_dict