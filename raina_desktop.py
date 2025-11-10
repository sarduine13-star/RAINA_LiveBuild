import sounddevice as sd
import numpy as np
import speech_recognition as sr
from openai import OpenAI
import requests, os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_ID = os.getenv("ELEVEN_VOICE_ID", "uyxf8x9s")

def speak_elevenlabs(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {"xi-api-key": ELEVEN_API_KEY, "Content-Type": "application/json"}
    payload = {"text": text, "model_id": "eleven_multilingual_v2"}
    r = requests.post(url, headers=headers, json=payload)
    if r.status_code == 200:
        with open("raina_reply.mp3", "wb") as f:
            f.write(r.content)
        os.system("start raina_reply.mp3" if os.name == "nt" else "afplay raina_reply.mp3")

def listen(duration=5, samplerate=16000):
    print("🎤 Listening...")
    rec = sr.Recognizer()
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype="int16")
    sd.wait()
    audio = sr.AudioData(audio_data.tobytes(), samplerate, 2)
    try:
        text = rec.recognize_google(audio)
        print(f"🗣️ You said: {text}")
        return text
    except sr.UnknownValueError:
        print("⚠️ Could not understand audio")
        return None

def main():
    print("🟣 RAINA voice mode active — Speak when ready.")
    while True:
        cmd = input("Press Enter to talk or Q to quit: ").strip().lower()
        if cmd == "q": break
        text = listen()
        if text:
            reply = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are RAINA, Red’s personal AI assistant."},
                    {"role": "user", "content": text}
                ]
            ).choices[0].message.cont
