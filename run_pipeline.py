import subprocess
import sys
import logging
from datetime import datetime

# Set up clean logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_command(command, description):
    logging.info(f"Starting: {description}...")
    # Run the shell command inside your virtual environment
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        logging.info(f"Success: {description}")
        if result.stdout:
            print(result.stdout.strip())
    else:
        logging.error(f"Failed: {description}")
        logging.error(result.stderr)
        sys.exit(1)

if __name__ == "__main__":
    logging.info("=== STARTING CRYPTO PIPELINE RUN ===")
    
    # 1. Run the python ingestion script using the venv interpreter
    run_command(".venv/bin/python ingest.py", "API Ingestion to Postgres Raw Schema")
    
    # 2. Run SQLMesh plan with auto-apply to compile and run downstream models
    run_command(".venv/bin/sqlmesh plan local --auto-apply --no-prompts", "SQLMesh Transformation and Mart Refresh")
    
    logging.info("=== CRYPTO PIPELINE RUN COMPLETE ===")