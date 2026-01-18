# US Economic Indicator Dashboard (2026)
*This project is automated via GitHub Actions to refresh data daily at [Your Time] EST.*

# 📈 Live Dashboard: [Click Here to View](https://econ-dashboard-2026.streamlit.app/)

A professional data pipeline and interactive dashboard that tracks key economic indicators using the Bureau of Labor Statistics (BLS) API.

## 🚀 Features
- **Automated Ingestion:** Fetches real-time data for Inflation (CPI), Employment (CES), and Labor Force (Unemployment).
- **Data Transformation:** Cleans raw JSON/CSV data and calculates Year-over-Year changes and monthly job gains.
- **Interactive Visualization:** A Streamlit-based dashboard for exploring economic trends.

## 🧰 Tech Stack
- **Python 3.11+**
- **Pandas:** For complex data manipulation and time-series analysis.
- **Plotly:** For interactive, responsive financial charting.
- **Streamlit:** For the frontend dashboard and deployment.
- **Python-Dotenv:** For secure API key management.

## 🛠️ Project Structure
- `src/ingest.py`: Scripts to fetch raw data from BLS.
- `src/transform.py`: Logic to clean and process data.
- `data/`: Local storage for raw and processed CSVs (data/raw/ ignored by Git).
- `run_pipeline.py`: The master script to update all data.

## Data Sources
- **Bureau of Labor Statistics (BLS) API:** [BLS Public Data API Documentation](https://www.bls.gov/developers/)
    *Economic Indicators Tracked:**
  - Consumer Price Index (CPI-U)
    - National CPI: (CUUR0000SA0)
    - Midwest CPI: (CUUR0200SA0)
  - Current Employment Statistics (CES)
    - US Employment: (CES0000000001)
    - MI Employment: (SMS26000000000000001)
  - Unemployment Rate
    - Current Population Survey (CPS)
    - Local Area Unemployment Statistics (LAUS)

## 🚦 Getting Started

### 1. Setup Environment
Ensure you have your `.env` file with your `BLS_KEY`.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
``` 

### 3. Update Data
To run the full ingestion and transformation pipeline, execute:
```bash
python run_pipeline.py
```
### 4. Launch Dashboard
To run launch the streamlit dashboard, execute:
```bash
streamlit run src/web/app.py
```

## 📊 Methodology
- **Ingestion:** Fetches JSON data via BLS API v2.
- **Transformation:** Data is cleaned, formatted, and new metrics (YoY change, monthly job gains) are calculated.
    - YoY Change: Calculated as ((Current / Value_12_Months_Ago) - 1) * 100
    - Monthly Job Gains: Calculated as Current_Month - Previous_Month (expressed in thousands).
- **Storage:** Data is stored in data/processed/ as flat CSVs to minimize API calls and improve dashboard load times.
- **Visualization:** Data is visualized using Plotly within a Streamlit app for interactivity.

## 🌐 Deployment
The dashboard is deployed on Streamlit Community Cloud and is automated by GitHub Actions to refresh data daily. The BLS API key is securely managed using GitHub Secrets.
If you would like to deploy your own version, follow these steps:
1. Fork this repository.
2. Set up a Streamlit Community Cloud account.
3. Connect your forked repository to Streamlit.
4. Add your BLS_KEY as a secret in both GitHub Actions (for the data pipeline) and Streamlit Cloud (if the app needs to access the API directly).
5. Deploy the app.