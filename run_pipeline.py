# Complete data pipeline script to run ingestion and transformation steps
import subprocess

def run_step(script_path):
    print(f"\n🚀 Running: {script_path}")
    result = subprocess.run(["python", script_path], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ {script_path} completed successfully.")
    else:
        print(f"❌ Error in {script_path}:\n{result.stderr}")

if __name__ == "__main__":
    print("--- Starting Economic Data Pipeline ---")

    # Define paths relative to the root
    run_step("src/ingest.py")
    run_step("src/transform.py")
    
    print("\n🎉 DATA UPDATED!")
    print("👉 To view the dashboard, run: streamlit run src/web/app.py")
