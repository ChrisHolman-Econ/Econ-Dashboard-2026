import streamlit as st
import pandas as pd
from pathlib import Path

# --- PAGE CONFIG ---
st.set_page_config(page_title="Econ Dashboard 2026", layout="wide")

# --- PATH SETUP ---
# Remember our "Ladder": src/web/app.py -> src/ -> Root -> data/processed/
root = Path(__file__).resolve().parent.parent.parent
processed_data_path = root / "data" / "processed"

# --- HEADER ---
st.title("📈 US Economic Indicators Dashboard")
st.markdown("Real-time data tracking from the Bureau of Labor Statistics.")

# --- DATA LOADING ---
try:
    inflation_df = pd.read_csv(processed_data_path / "inflation_cleaned.csv")
    st.success("Successfully loaded Inflation data!")
    
    # Show the first few rows (The 'View' equivalent)
    st.subheader("Inflation Data Preview")
    st.dataframe(inflation_df.head())
    
except Exception as e:
    st.error(f"Could not find data. Did you run the pipeline? Error: {e}")


