from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from openai import OpenAI
from dotenv import load_dotenv
from gtts import gTTS
import os, time

# --- Try to safely load pygame ---
try:
    import pygame
    PYGAME_AVAILABLE = True
except Exception:
    PYGAME_AVAILABLE = False

# --- Load environment variables ---
load_dotenv(dotenv_path=r"C:\RAINA_LiveBuild\.env", override=True)

app = FastAPI(title="RAINA Live Backend", version="1.0")

# --- Chat message schema ---
class ChatRequest(BaseModel):
    message: str

# --- Main chat endpoint ---
@app.post("/api/raina_chat")
async def raina_chat(req: ChatRequest):
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # --- Get AI reply ---
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are RAINA, Red’s intelligent assistant. Speak casually and helpfully."},
                {"role": "user", "content": req.message},
            ],
        )
        reply = completion.choices[0].message.content.strip()

        # --- Voice generation ---
        tts = gTTS(text=reply, lang="en")
        file_path = "raina_reply.mp3"
        tts.save(file_path)

        # --- Play audio (safe mode for Render) ---
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.init()
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(0.5)
                pygame.mixer.quit()
            except Exception as e:
                print(f"[AUDIO WARNING] Could not play sound: {e}")
        else:
            print("[INFO] Audio playback skipped (Render environment detected).")

        return {"response": reply, "audio_file": file_path}

    except Exception as e:
        return {"error": str(e)}

# --- Root endpoint for Render health check ---
@app.get("/")
async def root():
    env_status = "Local Mode" if os.getenv("RENDER") is None else "Render Mode"
    return {
        "status": "RAINA Live",
        "endpoint": "/api/raina_chat",
        "environment": env_status,
        "message": "Backend operational and connected."
    }

# --- Local run handler ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
