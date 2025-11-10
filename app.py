from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import requests
import os

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
# Use Render’s injected environment variables when deployed.
# Local override only if file exists.
load_dotenv(dotenv_path=r"C:\RAINA_LiveBuild\.env", override=True)

# --------------------------------------------------
# Initialize FastAPI
# --------------------------------------------------
app = FastAPI(
    title="RAINA Live API",
    description="Backend service for RAINA automation and BotGuardPro integration.",
    version="1.0.0"
)

# --------------------------------------------------
# Health Check Route
# --------------------------------------------------
@app.get("/")
def root():
    """
    Health route for Render / uptime checks.
    Does not expose secrets or logic.
    """
    return {
        "status": "RAINA Live",
        "endpoint": "/api/raina_chat",
        "message": "Backend operational and connected."
    }

# --------------------------------------------------
# Chat Request Model
# --------------------------------------------------
class ChatRequest(BaseModel):
    message: str

# --------------------------------------------------
# RAINA Chat Endpoint
# --------------------------------------------------
@app.post("/api/raina_chat")
async def raina_chat(req: ChatRequest):
    """
    Accepts a message, sends it to OpenAI, and returns RAINA's response.
    Optionally triggers Render redeploy if API keys are set.
    """
    try:
        # --- Chat Completion ---
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are RAINA, Red’s live AI assistant."},
                {"role": "user", "content": req.message},
            ]
        )
        reply = completion.choices[0].message.content

        # --- Optional Render Redeploy ---
        render_api_key = os.getenv("RENDER_API_KEY")
        render_service_id = os.getenv("RENDER_SERVICE_ID")

        if render_api_key and render_service_id:
            resp = requests.post(
                f"https://api.render.com/v1/services/{render_service_id}/deploys",
                headers={"Authorization": f"Bearer {render_api_key}"}
            )
            if resp.status_code == 201:
                redeploy_msg = "Render redeploy triggered successfully."
            else:
                redeploy_msg = f"Render redeploy error: {resp.text}"
        else:
            redeploy_msg = "Render credentials missing; skipped redeploy."

        # --- Final Response ---
        return {
            "status": "success",
            "message": reply,
            "redeploy": redeploy_msg
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

# --------------------------------------------------
# Local Dev Entry Point
# --------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
