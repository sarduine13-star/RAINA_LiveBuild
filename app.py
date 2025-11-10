from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from gtts import gTTS
import base64
from io import BytesIO

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/api/raina_chat")
async def raina_chat(request: Request):
    data = await request.json()
    msg = data.get("message", "")
    tts = gTTS(f"RAINA says: {msg}")
    buf = BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    audio = base64.b64encode(buf.read()).decode()
    return JSONResponse({ "text": msg, "audio": audio })
