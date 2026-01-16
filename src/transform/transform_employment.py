# Transform CES employment data for analysis
import pandas as pd
from pathlib import Path

# Path setup
root = Path(__file__).resolve().parent.parent.parent
input_file = root / "data" / "raw" / "employment_raw.csv"
output_file = root / "data" / "processed" / "employment_cleaned.csv"

def transform():
    df = pd.read_csv(input_file)
    
    # 1. Create the date column
    df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['period'].str.replace('M', '') + '-01')
    df = df.sort_values('date')
    
    # 2. Rename the raw value
    df = df.rename(columns={'value': 'total_nonfarm_employment'})
    
    # 3. CALCULATE THE GAIN (The missing piece!)
    # .diff() subtracts the previous row from the current row
    df['monthly_gain'] = df['total_nonfarm_employment'].diff()
    
    # 4. Clean up
    # Note: The very first row will be NaN because there's no previous month to subtract from.
    # We can either keep it or drop it. Let's keep it for now.
    final_df = df[['date', 'total_nonfarm_employment', 'monthly_gain']]
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(output_file, index=False)
    print(f"Employment transformation complete. Calculated gains saved to {output_file}")

if __name__ == "__main__":
    transform()