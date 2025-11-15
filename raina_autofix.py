import os, requests, time

# --- Verify critical vars ---
RENDER_KEY = os.getenv("RENDER_API_KEY")
BACKEND_URL = os.getenv("BACKEND_URL")
SITE_ID = os.getenv("RENDER_SITE_ID")
FRONTEND_ID = os.getenv("RENDER_FRONTEND_SERVICE_ID")

print("\n[RAINA-AUTOFIX] Starting full system sync...")
print(f"Backend URL: {BACKEND_URL}")
print(f"Render Site ID: {SITE_ID}")
print(f"Frontend ID: {FRONTEND_ID}")

# --- 1. Trigger backend redeploy ---
r1 = requests.post(
    f"https://api.render.com/v1/services/{SITE_ID}/deploys",
    headers={"Authorization": f"Bearer {RENDER_KEY}"},
    json={"clearCache": True},
)
print("Backend redeploy:", r1.status_code, r1.text[:120])

# --- 2. Trigger frontend redeploy ---
r2 = requests.post(
    f"https://api.render.com/v1/services/{FRONTEND_ID}/deploys",
    headers={"Authorization": f"Bearer {RENDER_KEY}"},
    json={"clearCache": True},
)
print("Frontend redeploy:", r2.status_code, r2.text[:120])

# --- 3. Wait for backend health ---
print("\nChecking backend health...")
for _ in range(12):  # up to ~1 min
    try:
        res = requests.get(f"{BACKEND_URL}/raina_admin", timeout=8)
        if res.status_code == 200:
            print("✅ RAINA backend online:", res.json())
            break
    except Exception:
        pass
    time.sleep(5)
else:
    print("⚠️ Backend not responding yet.")

# --- 4. Confirm front-end response ---
try:
    res = requests.get("https://botguardpro.com", timeout=10)
    print("✅ Front-end reachable" if res.status_code == 200 else f"⚠️ Front-end {res.status_code}")
except Exception as e:
    print("❌ Front-end check failed:", e)

print("\n[RAINA-AUTOFIX] Complete.")
