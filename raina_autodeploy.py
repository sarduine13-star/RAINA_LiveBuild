import os, subprocess, requests, time
from dotenv import load_dotenv

load_dotenv()

RENDER_API_KEY = os.getenv("RENDER_API_KEY")
SERVICE_NAME = "RAINA_LiveBuild"  # your Render service name

# 1. Local smoke test
print("\n=== Running Local Test ===")
os.environ["SDL_AUDIODRIVER"] = "dummy"
try:
    subprocess.run(["python", "app.py"], timeout=5)
except subprocess.TimeoutExpired:
    print("Local test passed (auto-stopped).")

# 2. Git push
print("\n=== Syncing with GitHub ===")
subprocess.run(["git", "add", "."], check=False)
subprocess.run(["git", "commit", "-m", "Auto Deploy RAINA"], check=False)
subprocess.run(["git", "push", "origin", "main"], check=False)

# 3. Render deploy
print("\n=== Deploying to Render ===")
headers = {"Authorization": f"Bearer {RENDER_API_KEY}"}
resp = requests.get("https://api.render.com/v1/services", headers=headers)
services = resp.json()

service_id = None
for s in services:
    if SERVICE_NAME.lower() in s["service"]["name"].lower():
        service_id = s["service"]["id"]
        break

if not service_id:
    raise Exception(f"Service '{SERVICE_NAME}' not found on Render.")

deploy_url = f"https://api.render.com/v1/services/{service_id}/deploys"
r = requests.post(deploy_url, headers=headers)
print(f"Triggered Render deploy: {r.status_code}")
print(r.text)
