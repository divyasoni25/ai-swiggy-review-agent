from fastapi import FastAPI
import threading
import subprocess
import sys
import os

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Review Agent"}

def run_pipeline():
    try:
        python_path = sys.executable
        script_path = os.path.join(os.getcwd(), "main.py")
        
        print("Starting pipeline...")
        subprocess.run([python_path, script_path])
        print("Pipeline finished")
    except Exception as e:
        print("Error running pipeline:", e)

@app.get("/run")
def run_agent():
    thread = threading.Thread(target=run_pipeline)
    thread.start()
    return {"status": "started in background"}