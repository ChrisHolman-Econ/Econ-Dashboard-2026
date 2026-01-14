import pandas as pd
import requests
import os
from dotenv import load_dotenv
from pathlib import Path

# Find the project root (up one level from 'src' where this file lives)
# This ensures it always finds the .env in Econ-Dashboard-2026/
base_dir = Path(__file__).resolve().parent.parent
load_dotenv(base_dir / ".env")

BLS_KEY = os.getenv("BLS_KEY")

def fetch_bls_data(series_ids, start_year, end_year):
    """
    Standardizes the BLS API call for any project script.
    """
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    payload = {
        "seriesid": series_ids,
        "startyear": str(start_year),
        "endyear": str(end_year),
        "registrationKey": BLS_KEY
    }
    
    response = requests.post(url, json=payload)
    data = response.json()
    
    # Error handling for API limits or key issues
    if 'Results' not in data:
        raise ValueError(f"API Error: {data.get('message', 'Unknown error')}")

    all_series = []
    for s in data['Results']['series']:
        temp_df = pd.DataFrame(s['data'])
        temp_df['series_id'] = s['seriesID']
        all_series.append(temp_df)
    
    df = pd.concat(all_series)

    # The clean date logic we perfected
    date_series = df['year'] + " " + df['periodName'].str[:3] + " 1"
    df['date'] = pd.to_datetime(date_series, format='%Y %b %d')
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    
    return df.dropna(subset=['value']).sort_values(['series_id', 'date'])