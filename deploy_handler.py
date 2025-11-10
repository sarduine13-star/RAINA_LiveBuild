import os
import requests
import subprocess
from datetime import datetime
from fastapi import FastAPI

app = FastAPI()

RENDER_DEPLOY_URL = os.getenv("RENDER_DEPLOY_URL")
RENDER_API_KEY = os.getenv("RENDER_API_KEY")
GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

@app.get("/api/deploy")
def manual_deploy():
    """Triggers both GitHub push and Render deploy"""
    try:
        # 1. Commit any local changes
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"Auto-deploy {datetime.now()}"], check=False)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("✅ GitHub push complete")

        # 2. Trigger Render deploy
        if RENDER_DEPLOY_URL and RENDER_API_KEY:
            resp = requests.post(
                RENDER_DEPLOY_URL,
                headers={
                    "Authorization": f"Bearer {RENDER_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={}
            )
            if resp.status_code in (200, 201):
                return {"status": "success", "message": "Render deploy triggered"}
            else:
                return {"status": "error", "details": resp.text}
        else:
            return {"status": "error", "details": "Missing Render API vars"}

    except subprocess.CalledProcessError as e:
        return {"status": "error", "details": f"Git push failed: {e}"}
    except Exception as e:
        return {"status": "error", "details": str(e)}


@app.get("/api/status")
def check_status():
    """Checks deploy and connection status"""
    return {
        "raina": "online",
        "timestamp": datetime.now().isoformat(),
        "github_key_set": bool(GITHUB_ACCESS_TOKEN),
        "render_key_set": bool(RENDER_API_KEY),
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
