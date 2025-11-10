import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from gtts import gTTS

# ✅ Load environment
load_dotenv()

# ✅ FastAPI app
app = FastAPI(title="RAINA Backend", version="1.0")

# ✅ CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Health check
@app.get("/api/info")
def info():
    return {
        "environment": "Render",
        "stripe_key_set": bool(os.getenv("STRIPE_SECRET_KEY")),
        "pygame_enabled": False
    }

# ✅ Request model
class ChatRequest(BaseModel):
    message: str

# ✅ Voice synthesis
def synth_audio(text: str) -> str:
    tts = gTTS(text)
    tts.save("raina.mp3")
    with open("raina.mp3", "rb") as f:
        return f.read().hex()

# ✅ RAINA chat route
@app.post("/api/raina_chat")
async def raina_chat(req: ChatRequest):
    msg = req.message.strip()
    if not msg:
        return JSONResponse({ "text": "Say something first, partner." }, status_code=400)

    reply = f"RAINA heard: {msg}"
    audio_hex = synth_audio(reply)

    return { "text": reply, "audio_b64": audio_hex }

# ✅ Local run block (Render uses its own entrypoint)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
