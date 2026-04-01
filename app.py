from fastapi import FastAPI
import subprocess

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Review Agent"}

@app.get("/run")
def run_agent():
    result = subprocess.run(["python", "main.py"], capture_output=True, text=True)
    return {
        "status": "completed",
        "output": result.stdout,
        "error": result.stderr
    }