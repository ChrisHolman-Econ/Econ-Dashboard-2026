# Transform CES employment data for analysis
import pandas as pd
import os

# Load employment data from saved file
df = pd.read_csv("data/raw/employment_raw.csv")

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Sort by date
df = df.sort_values('date').reset_index(drop=True)

# Select only date and value columns (rename value to employment)
df_clean = df[['date', 'value']].copy()
df_clean.columns = ['date', 'total_nonfarm_employment']

# Display results
print(df_clean.head(15))
print("\n")
print(df_clean.tail(10))

# Save processed data
output_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed", "employment_cleaned.csv")
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df_clean.set_index('date').to_csv(output_path)
print(f"\nData saved to {output_path}")