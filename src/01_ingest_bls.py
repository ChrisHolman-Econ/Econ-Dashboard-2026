# Import Libraries
import pandas as pd
import numpy as np
import requests
import os
from io import StringIO

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
    df['value'] = pd.to_numeric(df['value'])
    
    # Select Relevant Columns
    df = df[['date', 'value']]
    
    return df

# Set Parameters
series = "CUUR0000SA0"  # Example Series ID for All Urban Consumers
start_year = 2015
end_year = 2025

# extract data
ingest_bls_data(series, start_year, end_year)









