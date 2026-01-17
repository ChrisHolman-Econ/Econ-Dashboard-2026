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
    
    fig_emp.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(count=3, label="3y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    st.plotly_chart(fig_emp, use_container_width=True)
    
    with st.expander("View Raw Data Table"):
        st.dataframe(df_emp)

elif page == "Labor Force":
    st.header("Unemployment Rate")

# Load the labor force data
df_labor = pd.read_csv(processed_data_path / "laborforce_cleaned.csv")
df_labor['date'] = pd.to_datetime(df_labor['date'])

# Create a Line Chart for unemployment rate
fig_labor = px.line(df_labor, x='date', y='unemployment_rate',
                    title="Unemployment Rate Trend",
                    labels={'unemployment_rate': 'Unemployment Rate (%)', 'date': 'Month'},
                    markers=True)

# Add horizontal line for reference (e.g., 5% unemployment)
fig_labor.add_hline(y=4.0, line_dash="dash", line_color="red",
                     annotation_text="4% Reference Line", 
                     annotation_position="top left")

st.plotly_chart(fig_labor, use_container_width=True)
                    
# --- GLOBAL METRICS ---
# Retreive most recent value from each dataframe
if page == "Inflation (CPI)":  
    # Pull the last row's inflation value
    df_inf = pd.read_csv(processed_data_path / "inflation_cleaned.csv")
    current_val = df_inf['yoy_inflation_rate'].iloc[-1]                     
    previous_val = df_inf['yoy_inflation_rate'].iloc[-2]
    delta = current_val - previous_val
    
    st.metric(
        label="Current YoY Inflation Rate (%)", 
        value=f"{current_val:.1f}%", 
        delta = f"{delta:.1f} vs Last Month",
        delta_color="inverse"
        )

elif page == "Employment (CES)":
    df_emp = pd.read_csv(processed_data_path / "employment_cleaned.csv")
    current_val = df_emp['monthly_gain'].iloc[-1]
    previous_val = df_emp['monthly_gain'].iloc[-2]
    delta = current_val - previous_val
    
    st.metric(
        label="Latest Monthly Job Gain/Loss", 
        value=f"{current_val:,.0f}",
        delta=f"{delta:,.0f} vs Last Month"
    )
              

elif page == "Labor Force":
    df_laborforce = pd.read_csv(processed_data_path / "laborforce_cleaned.csv")
    current_val = df_laborforce['unemployment_rate'].iloc[-1]
    previous_val = df_laborforce['unemployment_rate'].iloc[-2]
    delta = current_val - previous_val
    
    st.metric(
        label="Current Unemployment Rate (%)", 
        value=f"{current_val:.1f}%", 
        delta=f"{delta}%",
        delta_color="inverse"
    )

# --- SIDEBAR FOOTER ---
st.sidebar.markdown("---")
st.sidebar.write("### ABOUT")
st.sidebar.info(
    """
    This dashboard is powered by the **BLS Public Data API**.
    It automatically updates with the latest economic indicators.
    """
)
