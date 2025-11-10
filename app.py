from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from openai import OpenAI
from dotenv import load_dotenv
from gtts import gTTS
import pygame, os, time, stripe

# === Load Environment Variables ===
load_dotenv(dotenv_path=r"C:\RAINA_LiveBuild\.env", override=True)

# === Initialize Stripe ===
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
stripe.api_key = STRIPE_SECRET_KEY

# === Initialize FastAPI App ===
app = FastAPI(title="RAINA + Stripe Backend")

# === RAINA Chat Request Model ===
class ChatRequest(BaseModel):
    message: str

@app.post("/api/raina_chat")
async def raina_chat(req: ChatRequest):
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are RAINA, Red’s live AI assistant."},
                {"role": "user", "content": req.message},
            ],
        )
        reply = completion.choices[0].message.content

        # Voice reply
        tts = gTTS(text=reply, lang='en')
        file_path = "raina_reply.mp3"
        tts.save(file_path)

        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.5)
        pygame.mixer.quit()

        return {"response": reply, "audio_file": file_path}

    except Exception as e:
        return {"error": str(e)}

# === Stripe Payment Test Endpoint ===
@app.get("/api/stripe/test")
async def stripe_test():
    try:
        balance = stripe.Balance.retrieve()
        return {"status": "Connected ✅", "available": balance["available"]}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# === Stripe Checkout Session Creator ===
@app.post("/api/create-checkout-session")
async def create_checkout_session(request: Request):
    try:
        data = await request.json()
        price_id = data.get("price_id")

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": price_id, "quantity": 1}],
            mode="subscription",
            success_url="https://botguardpro-site.onrender.com/success",
            cancel_url="https://botguardpro-site.onrender.com/cancel",
        )
        return {"url": session.url}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

# === Root Route ===
@app.get("/")
async def root():
    return {"status": "RAINA + Stripe Live", "message": "Backend operational and connected."}
