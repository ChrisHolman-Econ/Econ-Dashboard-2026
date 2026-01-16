import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --- PAGE CONFIG ---
st.set_page_config(page_title="Econ Dashboard 2026", layout="wide")

# --- PATH SETUP ---
root = Path(__file__).resolve().parent.parent.parent
processed_data_path = root / "data" / "processed"

# --- SIDEBAR NAV ---
st.sidebar.header("Navigation")
page = st.sidebar.selectbox("Choose a Metric", ["Inflation (CPI)", "Employment (CES)", "Labor Force"])

# --- HEADER ---
st.title("📈 US Economic Indicators")

# --- LOGIC FOR INFLATION ---
if page == "Inflation (CPI)":
    st.header("Consumer Price Index (YoY % Change)")
    
    df = pd.read_csv(processed_data_path / "inflation_cleaned.csv")
    df['date'] = pd.to_datetime(df['date']) # Ensure date is a datetime object
    
    # Create the Plotly Chart (The 'ggplot' equivalent)
    fig = px.line(df, x='date', y='yoy_inflation_rate', 
                 title="Inflation Trend",
                 labels={'yoy_inflation': 'YoY % Change', 'date': 'Month'},
                 markers=True)
    
    # Show the chart
    st.plotly_chart(fig, use_container_width=True)
    
    # Show data table below if interested
    with st.expander("View Raw Data Table"):
        st.dataframe(df)

# --- PLACEHOLDERS FOR OTHER PAGES ---
elif page == "Employment (CES)":
    st.header("Monthly Non-Farm Payroll Gains/Losses")
    
    # Load the employment data
    df_emp = pd.read_csv(processed_data_path / "employment_cleaned.csv")
    df_emp['date'] = pd.to_datetime(df_emp['date'])
    
    # Create a Bar Chart for job gains
    # We use a color scale so gains are blue and any losses would be red
    fig_emp = px.bar(df_emp, x='date', y='monthly_gain',
                    title="Monthly Job Growth",
                    labels={'monthly_gain': 'Jobs Gained/Lost (thousands)', 'date': 'Month'},
                    color='monthly_gain',
                    color_continuous_scale='RdBu')
    
    st.plotly_chart(fig_emp, use_container_width=True)
    
    with st.expander("View Raw Data Table"):
        st.dataframe(df_emp)

elif page == "Labor Force":
    st.header("Unemployment Rate")
    st.info("We will add the Unemployment line chart here next.")