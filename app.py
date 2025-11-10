from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, FileResponse
from openai import OpenAI
from dotenv import load_dotenv
from gtts import gTTS
import pygame, time, os

# --- Load environment variables ---
load_dotenv(dotenv_path=r"C:\RAINA_LiveBuild\.env", override=True)

app = FastAPI()

# --- Chat model for requests ---
class ChatRequest(BaseModel):
    message: str

# --- Core RAINA endpoint ---
@app.post("/api/raina_chat")
async def raina_chat(req: ChatRequest):
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are RAINA, Red’s live AI assistant and automation agent."},
                {"role": "user", "content": req.message},
            ],
        )
        reply = completion.choices[0].message.content

        # --- Generate voice output ---
        tts = gTTS(text=reply, lang='en')
        file_path = "raina_reply.mp3"
        tts.save(file_path)

        # --- Auto-play reply (optional when local only) ---
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.5)
            pygame.mixer.quit()
        except Exception:
            pass

        return {"response": reply, "audio_file": file_path}

    except Exception as e:
        return {"error": str(e)}

# --- Serve audio files if needed ---
@app.get("/audio/{filename}")
async def get_audio(filename: str):
    file_path = os.path.join(os.getcwd(), filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mpeg")
    return {"error": "File not found"}

# --- RAINA chat overlay ---
@app.get("/", response_class=HTMLResponse)
async def chat_page():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RAINA Live Chat</title>
    <style>
    body {
      background-color: #0f0f0f;
      color: #f2f2f2;
      font-family: Arial, sans-serif;
      display: flex;
      flex-direction: column;
      height: 100vh;
      margin: 0;
    }
    #chat-box {
      flex: 1;
      overflow-y: auto;
      padding: 20px;
    }
    .message {
      margin: 8px 0;
      padding: 10px 14px;
      border-radius: 8px;
      max-width: 75%;
    }
    .user { background-color: #1f6feb; align-self: flex-end; }
    .raina { background-color: #222; }
    #input-area {
      display: flex;
      padding: 10px;
      background-color: #111;
    }
    #message {
      flex: 1;
      padding: 8px;
      border: none;
      border-radius: 4px;
    }
    #send {
      margin-left: 10px;
      padding: 8px 14px;
      background-color: #1f6feb;
      color: #fff;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
    </style>
    </head>
    <body>
      <div id="chat-box"></div>
      <div id="input-area">
        <input id="message" type="text" placeholder="Talk to RAINA..." />
        <button id="send">Send</button>
      </div>

    <script>
    const API_URL = window.location.origin + "/api/raina_chat";
    const chatBox = document.getElementById('chat-box');
    const input = document.getElementById('message');
    const sendBtn = document.getElementById('send');

    function addMessage(text, sender) {
      const div = document.createElement('div');
      div.classList.add('message', sender);
      div.textContent = text;
      chatBox.appendChild(div);
      chatBox.scrollTop = chatBox.scrollHeight;
    }

    async function sendMessage() {
      const msg = input.value.trim();
      if (!msg) return;
      addMessage(msg, 'user');
      input.value = '';
      try {
        const res = await fetch(API_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: msg })
        });
        const data = await res.json();
        addMessage(data.response || data.error || "No reply", 'raina');
      } catch (err) {
        addMessage("Error: " + err.message, 'raina');
      }
    }

    sendBtn.onclick = sendMessage;
    input.addEventListener('keypress', e => { if (e.key === 'Enter') sendMessage(); });
    </script>
    </body>
    </html>
    """
