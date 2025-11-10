import os
import time
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=r"C:\\RAINA_LiveBuild\\.env", override=True)

def check_service(name, url, headers=None):
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            print(f"✅ {name} online ({r.status_code})")
        else:
            print(f"⚠️ {name} returned {r.status_code}")
    except Exception as e:
        print(f"❌ {name} check failed: {e}")

def check_render():
    check_service("Render Site", "https://raina-cco5.onrender.com/health")

def check_brevo():
    key = os.getenv("BREVO_API_KEY")
    if not key:
        print("⚠️ Brevo key missing")
        return
    headers = {"api-key": key}
    check_service("Brevo", "https://api.brevo.com/v3/contacts", headers)

def check_apollo():
    key = os.getenv("APOLLO_API_KEY")
    if not key:
        print("⚠️ Apollo key missing")
        return
    headers = {"Authorization": f"Bearer {key}"}
    check_service("Apollo", "https://api.apollo.io/v1/auth/identify_user", headers)

def check_stripe():
    key = os.getenv("STRIPE_SECRET_KEY")
    if not key:
        print("⚠️ Stripe key missing")
        return
    try:
        r = requests.get("https://api.stripe.com/v1/charges", auth=(key, ""))
        print("✅ Stripe reachable" if r.status_code == 200 else f"⚠️ Stripe {r.status_code}")
    except Exception as e:
        print(f"❌ Stripe check failed: {e}")

def check_make():
    key = os.getenv("MAKE_API_KEY")
    if not key:
        print("⚠️ Make API key missing")
        return
    headers = {"Authorization": f"Token {key}"}
    check_service("Make.com", "https://us2.make.com/api/v2/scenarios", headers)

def update_stripe_site():
    try:
        render_service_id = os.getenv("RENDER_SERVICE_ID")
        render_api_key = os.getenv("RENDER_API_KEY")
        stripe_key = os.getenv("STRIPE_SECRET_KEY")

        # 1. Trigger Render redeploy
        r = requests.post(
            f"https://api.render.com/v1/services/{render_service_id}/deploys",
            headers={"Authorization": f"Bearer {render_api_key}"}
        )
        if r.status_code == 201:
            print("✅ Render site redeploy triggered.")
        else:
            print(f"⚠️ Render redeploy failed: {r.text}")

        # 2. Verify Stripe connection
        s = requests.get("https://api.stripe.com/v1/charges", auth=(stripe_key, ""))
        print("✅ Stripe connection verified" if s.status_code == 200 else f"⚠️ Stripe error: {s.status_code}")

    except Exception as e:
        print(f"❌ update_stripe_site failed: {e}")

# ---- Main loop ----
while True:
    print("\n--- RAINA Stack Health + Site Update ---")
    check_render()
    check_brevo()
    check_apollo()
    check_stripe()
    check_make()
    update_stripe_site()
    print("----------------------------------------")
    time.sleep(1800)  # every 30 minutes
