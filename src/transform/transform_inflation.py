# Clean the CPI data and calculate inflation rates from 01_ingest_bls.py
# Import Libraries
import pandas as pd
import os

# Load CPI data from saved file
df = pd.read_csv("data/raw/inflation_raw.csv")

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Sort by date to ensure proper calculation
df = df.sort_values('date').reset_index(drop=True)

# Calculate Month-to-Month Inflation Rate
# Formula: ((Current Month - Previous Month) / Previous Month) * 100
df['mom_inflation_rate'] = df['value'].pct_change() * 100

# Calculate Annualized Month-to-Month Inflation Rate
# Formula: ((1 + monthly_rate/100)^12 - 1) * 100
df['mom_annualized_rate'] = ((1 + df['mom_inflation_rate'] / 100) ** 12 - 1) * 100

# Calculate 12-Month (Year-over-Year) Inflation Rate
# Formula: ((Current Month - 12 Months Ago) / 12 Months Ago) * 100
df['yoy_inflation_rate'] = df['value'].pct_change(periods=12) * 100

# Round to 2 decimal places for readability
df['mom_inflation_rate'] = df['mom_inflation_rate'].round(2)
df['mom_annualized_rate'] = df['mom_annualized_rate'].round(2)
df['yoy_inflation_rate'] = df['yoy_inflation_rate'].round(2)

# Display results
print(df.head(15))
print("\n")
print(df.tail(10))

# Save processed data
output_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed", "inflation_cleaned.csv")
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df.to_csv(output_path, index=False)
print(f"\nData saved to {output_path}")