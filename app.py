# Deploy trigger — RAINA backend overlay confirmed

import os
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import stripe

# ✅ Load environment
load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# ✅ FastAPI app
app = FastAPI(title="RAINA LiveBuild API", version="2.1")

# ✅ CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Health check
@app.get("/")
def root():
    return { "status": "Online ✅", "service": "RAINA + Stripe Integration" }

@app.get("/api/status")
def status():
    return { "raina": "active", "timestamp": time.strftime("%Y-%m-%d %H:%M:%S") }

@app.get("/api/info")
def info():
    return {
        "environment": "Render" if os.getenv("RENDER") == "true" else "Local",
        "stripe_key_set": bool(os.getenv("STRIPE_SECRET_KEY")),
        "pygame_enabled": False
    }

# ✅ Stripe test
@app.get("/api/stripe/test")
def stripe_test():
    try:
        balance = stripe.Balance.retrieve()
        return { "status": "Connected ✅", "available": balance.get("available") }
    except Exception as e:
        return JSONResponse(content={ "status": "Error ❌", "detail": str(e) }, status_code=500)

# ✅ RAINA chat route
class ChatRequest(BaseModel):
    message: str

@app.post("/api/raina_chat")
async def raina_chat(req: ChatRequest):
    msg = req.message.strip()
    if not msg:
        return JSONResponse({ "text": "Say something first, partner." }, status_code=400)

    # 🔁 Replace with actual AI + voice logic
    reply = f"RAINA heard: {msg}"
    audio_hex = ""  # Optional: hex-encoded MP3 string

    return { "text": reply, "audio_b64": audio_hex }

# ✅ Local run block (Render uses its own entrypoint)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
