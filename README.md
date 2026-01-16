# US Economic Indicator Dashboard (2026)

A professional data pipeline and interactive dashboard that tracks key economic indicators using the Bureau of Labor Statistics (BLS) API.

## 🚀 Features
- **Automated Ingestion:** Fetches real-time data for Inflation (CPI), Employment (CES), and Labor Force (Unemployment).
- **Data Transformation:** Cleans raw JSON/CSV data and calculates Year-over-Year changes and monthly job gains.
- **Interactive Visualization:** A Streamlit-based dashboard for exploring economic trends.

## 🛠️ Project Structure
- `src/ingest/`: Scripts to fetch raw data from BLS.
- `src/transform/`: Logic to clean and process data.
- `data/`: Local storage for raw and processed CSVs (ignored by Git).
- `run_pipeline.py`: The master script to update all data.

## 🚦 Getting Started

### 1. Setup Environment
Ensure you have your `.env` file with your `BLS_API_KEY`.

### 2. Update Data
To run the full ingestion and transformation pipeline, execute:
```bash
python run_pipeline.py
```
### 3. Launch Dashboard
(Coming Soon)
```bash
streamlit run src/web/app.py
```