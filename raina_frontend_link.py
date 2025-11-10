import os, requests

# Environment setup
render_api_key = os.getenv("RENDER_API_KEY")
frontend_service_id = "srv-d44gbbadbo4c73eulffg"
github_repo = "sarduine13-star/botguard-pro"

def trigger_frontend_redeploy():
    url = f"https://api.render.com/v1/services/{frontend_service_id}/deploys"
    headers = {"Authorization": f"Bearer {render_api_key}"}
    payload = {
        "clearCache": True,
        "commitMessage": f"Auto-redeploy triggered by RAINA for {github_repo}"
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print("✅ Frontend redeploy triggered successfully.")
    else:
        print(f"❌ Redeploy failed: {response.status_code} - {response.text}")

if __name__ == "__main__":
    trigger_frontend_redeploy()
