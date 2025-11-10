from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# ✅ CORS fix
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

# ✅ POST route for RAINA chat
@app.post("/api/raina_chat")
async def raina_chat(request: Request):
    data = await request.json()
    user_msg = data.get("message", "")
    
    # 🔁 Replace this with your actual RAINA logic
    reply_text = f"RAINA heard: {user_msg}"
    audio_hex = ""  # Optional: hex-encoded MP3 string

    return JSONResponse(content={ "text": reply_text, "audio_b64": audio_hex })
