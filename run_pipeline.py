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
    # --- STEP 1: INGESTION ---
    run_step("src/ingest/ingest_inflation.py")
    run_step("src/ingest/ingest_employment.py")
    run_step("src/ingest/ingest_laborforce.py")
    
    # --- STEP 2: TRANSFORMATION ---
    run_step("src/transform/transform_inflation.py")
    run_step("src/transform/transform_employment.py")
    run_step("src/transform/transform_laborforce.py")
    
    print("\n🎉 ALL STEPS COMPLETE. Data is ready for the dashboard.")
