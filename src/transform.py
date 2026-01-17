# Transform economic data for dashboard analysis
import pandas as pd
from pathlib import Path

# Define the pairs we want to join together
COMPARISON_MAP = {
    'inflation': ['US_Inflation', 'MI_Inflation'],
    'unemployment': ['US_Unemployment', 'MI_Unemployment'],
    'employment': ['US_Employment', 'MI_Employment']
}

def clean_data(df, label):
    """A small helper function to clean individual dataframes"""
    # Convert '3.5' string to 3.5 float
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    # Create a clean date column
    df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['periodName'] + '-01')
    # Keep only what we need and rename 'value' to something specific (like 'US_Inflation')
    return df[['date', 'value']].rename(columns={'value': label})

# THE LOOP:
for metric, files in COMPARISON_MAP.items():
    print(f"Combining {metric} data...")
    
    # 1. Load and clean the US file
    us_raw = pd.read_csv(f"data/raw/{files[0]}_raw.csv")
    us_clean = clean_data(us_raw, f"US_{metric}")
    
    # 2. Load and clean the MI file
    mi_raw = pd.read_csv(f"data/raw/{files[1]}_raw.csv")
    mi_clean = clean_data(mi_raw, f"MI_{metric}")
    
    # 3. GLUE THEM TOGETHER (The Join)
    # This aligns them perfectly by date
    merged = pd.merge(us_clean, mi_clean, on='date', how='outer').sort_values('date')
    
    # 4. Save the "Wide" comparison file
    merged.to_csv(f"data/processed/{metric}_comparison.csv", index=False)
    print(f"Saved: {metric}_comparison.csv")

# 1. Year-over-Year 
    merged[f'US_{metric}_YoY'] = merged[f'US_{metric}'].pct_change(periods=12) * 100
    merged[f'MI_{metric}_YoY'] = merged[f'MI_{metric}'].pct_change(periods=12) * 100

    # 2. Monthly Change (Specific for Employment)
    if metric == 'employment':
        # This calculates the raw difference (e.g., +5.2 thousand jobs)
        merged['US_Employment_Monthly'] = merged['US_employment'].diff()
        merged['MI_Employment_Monthly'] = merged['MI_employment'].diff()