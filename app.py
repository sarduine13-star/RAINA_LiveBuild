from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from gtts import gTTS
import base64

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/api/raina_chat")
async def raina_chat(request: Request):
    data = await request.json()
    msg = data.get("message", "")
    tts = gTTS(f"RAINA says: {msg}")
    tts.save("r.mp3")
    with open("r.mp3", "rb") as f:
        audio = base64.b64encode(f.read()).decode()
    return JSONResponse({ "text": msg, "audio": audio })
