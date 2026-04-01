from fastapi import FastAPI
import threading
import subprocess

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Review Agent"}

def run_pipeline():
    try:
        subprocess.run(["python", "main.py"])
    except Exception as e:
        print("Error running pipeline:", e)

@app.get("/run")
def run_agent():
    thread = threading.Thread(target=run_pipeline)
    thread.start()
    return {"status": "started in background"}