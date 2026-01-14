# Transform Labor Force data from long to wide format
# Each metric becomes a separate column with date as the index
import pandas as pd
import os

# Load labor force data from saved file
df = pd.read_csv("data/raw/bls_laborforce_raw.csv")

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Create a mapping for series_id to metric names
series_mapping = {
    'LNS11000000': 'labor_force',
    'LNS12000000': 'employment',    
    'LNS13000000': 'unemployment_number',
    'LNS14000000': 'unemployment_rate'
}

# Rename series_id using the mapping
df['metric'] = df['series_id'].map(series_mapping)

# Pivot to wide format with date as index and metrics as columns
df_wide = df.pivot_table(index='date', columns='metric', values='value', aggfunc='first')
df_wide = df_wide.reset_index()

# Reorder columns for clarity
column_order = ['date', 'labor_force', 'employment', 'unemployment_number', 'unemployment_rate']
df_wide = df_wide[[col for col in column_order if col in df_wide.columns]]

# Display results
print(df_wide.head(15))
print("\n")
print(df_wide.tail(10))

# Save processed data
output_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed", "laborforce_metric.csv")
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df_wide.to_csv(output_path, index=False)
print(f"\nData saved to {output_path}")
