import streamlit as st
import pandas as pd
import plotly.express as px
import os
import datetime as dt

st.set_page_config(page_title="Michigan Economic Dashboard", layout="wide")

st.title("📈 Michigan vs. US Economic Comparison")

# 1. SIDEBAR: Select the Metric
with st.sidebar:
    st.header("Dashboard Settings")
    
    # Show last updated timestamp
    target_file = 'data/processed/inflation_comparison.csv'
    if os.path.exists(target_file):
        mtime = os.path.getmtime(target_file)
        last_update = dt.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %I:%M %p')
        st.caption(f"Last Sync: {last_update} EST")
    
    st.divider()

    # Select Economic Indicator
    metric = st.selectbox(
        "Select Economic Indicator",
        options=["inflation", "unemployment", "employment"],
        format_func=lambda x: x.title()
    )
    
    # Toggle between Raw Data and Growth Rate
    view_mode = st.radio(
        "View Mode",
        options=["Raw Level", "Year-over-Year % Change"]
    )

# 2. LOAD DATA: Dynamically load based on selection
file_path = f"data/processed/{metric}_comparison.csv"
df = pd.read_csv(file_path)
df['date'] = pd.to_datetime(df['date'])

# 3. SELECT COLUMNS: Pick the right columns based on view_mode
if view_mode == "Year-over-Year % Change":
    y_cols = [f'US_{metric}_YoY', f'MI_{metric}_YoY']
    y_label = "Percentage Change (%)"
else:
    y_cols = [f'US_{metric}', f'MI_{metric}']
    y_label = "Value / Index Level"

# 4. PLOT: One chart to rule them all
fig = px.line(
    df, 
    x='date', 
    y=y_cols,
    title=f"{metric.title()} Comparison: US vs. Michigan",
    labels={"value": y_label, "date": "Date", "variable": "Region"},
    template="plotly_white"
)

if metric == 'employment':
    st.subheader("Monthly Job Gains & Losses")
    
    # We create a bar chart for the Michigan Monthly change
    fig_mo = px.bar(
        df, 
        x='date', 
        y='MI_Employment_Monthly',
        title="Michigan Monthly Net Job Change",
        color='MI_Employment_Monthly', # Color bars based on value
        color_continuous_scale='RdYlGn', # Red for losses, Green for gains
        labels={'MI_Employment_Monthly': 'Jobs (Thousands)'}
    )
    
    # Add a line at 0 to make losses obvious
    fig_mo.add_hline(y=0, line_color="black")
    
    st.plotly_chart(fig_mo, use_container_width=True)
    
# Add a horizontal line at 0 for % change charts
if view_mode == "Year-over-Year % Change":
    fig.add_hline(y=0, line_dash="dash", line_color="gray")

st.plotly_chart(fig, use_container_width=True)

# 5. DATA TABLE: Peek at the raw numbers
with st.expander("View Raw Data Table"):
    st.dataframe(df.sort_values('date', ascending=False), use_container_width=True)