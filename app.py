import os, requests, re, subprocess
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="RAINA LiveBuild")

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Root + status ---
@app.get("/")
def home():
    return {"message": "RAINA LiveBuild backend running"}

@app.get("/raina_admin")
def raina_admin():
    return {"status": "online", "service": "RAINA LiveBuild"}

# --- Deploy hook ---
@app.post("/update_frontend")
def update_frontend():
    render_key = os.getenv("RENDER_API_KEY")
    service_id = os.getenv("RENDER_SITE_ID")

    if not render_key or not service_id:
        return {"error": "Missing Render credentials"}

    r = requests.post(
        f"https://api.render.com/v1/services/{service_id}/deploys",
        headers={"Authorization": f"Bearer {render_key}"},
    )
    return {"status": r.status_code, "text": r.text}
