import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Michigan Economic Dashboard", layout="wide")

st.title("📈 Michigan vs. US Economic Comparison")

# 1. SIDEBAR: Select the Metric
with st.sidebar:
    st.header("Dashboard Settings")
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

# Optional: Add a horizontal line at 0 for % change charts
if view_mode == "Year-over-Year % Change":
    fig.add_hline(y=0, line_dash="dash", line_color="gray")

st.plotly_chart(fig, use_container_width=True)

# 5. DATA TABLE: Peek at the raw numbers
with st.expander("View Raw Data Table"):
    st.dataframe(df.sort_values('date', ascending=False), use_container_width=True)