from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import requests
import os

# Load environment variables
load_dotenv(dotenv_path=r"C:\RAINA_LiveBuild\.env", override=True)

app = FastAPI()

# Request model
class ChatRequest(BaseModel):
    message: str

@app.post("/api/raina_chat")
async def raina_chat(req: ChatRequest):
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

        # --- Optional Render redeploy ---
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

        # --- Final return payload ---
        return {
            "status": "success",
            "message": reply,
            "redeploy": redeploy_msg
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
