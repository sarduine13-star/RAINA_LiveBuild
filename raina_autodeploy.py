from fastapi import FastAPI
import os, requests, uvicorn
from dotenv import load_dotenv

# --- Auto-load environment variables from .env ---
load_dotenv(dotenv_path=r"C:\RAINA_LiveBuild\.env")

app = FastAPI()

# --- Pull API Keys and IDs ---
RENDER_API_KEY = os.getenv("RENDER_API_KEY")
FRONTEND_SERVICE_ID = os.getenv("FRONTEND_SERVICE_ID")

# --- Root test route ---
@app.get("/")
def root():
    return {"status": "RAINA AutoDeploy active"}

# --- Redeploy Trigger ---
@app.post("/redeploy")
def redeploy_frontend():
    if not RENDER_API_KEY or not FRONTEND_SERVICE_ID:
        return {"error": "Missing Render API key or Service ID"}

    url = f"https://api.render.com/v1/services/{FRONTEND_SERVICE_ID}/deploys"
    headers = {"Authorization": f"Bearer {RENDER_API_KEY}"}
    r = requests.post(url, headers=headers)

    if r.status_code == 201:
        return {"status": "triggered", "response": "Redeploy initiated on Render"}
    else:
        return {"status": "failed", "code": r.status_code, "response": r.text}

# --- Local run setup ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
