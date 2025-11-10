import os
import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# --- LOAD ENVIRONMENT VARIABLES ---
load_dotenv()

# --- STRIPE INITIALIZATION ---
import stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# --- HANDLE PYGAME (local only) ---
if os.getenv("RENDER") != "true":
    try:
        import pygame
        pygame.init()
        print("🎮 Pygame initialized locally.")
    except Exception as e:
        print("⚠️ Pygame failed to init:", e)
else:
    print("☁️ Running on Render: pygame disabled.")

# --- INITIALIZE FASTAPI APP ---
app = FastAPI(
    title="RAINA LiveBuild API",
    version="2.1",
    description="RAINA backend API with Stripe integration and chat endpoint."
)

# --- ROUTES ---

@app.get("/")
def root():
    """Root route for uptime check."""
    return {"status": "Online ✅", "service": "RAINA + Stripe Integration"}

@app.get("/api/stripe/test")
def stripe_test():
    """Check Stripe connection and balance availability."""
    try:
        balance = stripe.Balance.retrieve()
        return {"status": "Connected ✅", "available": balance.get("available")}
    except Exception as e:
        return JSONResponse(content={"status": "Error ❌", "detail": str(e)}, status_code=500)

@app.get("/api/status")
def status():
    """RAINA basic heartbeat."""
    return {"raina": "active", "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}

@app.get("/api/info")
def info():
    """System/environment info."""
    return {
        "environment": "Render" if os.getenv("RENDER") == "true" else "Local",
        "stripe_key_set": bool(os.getenv("STRIPE_SECRET_KEY")),
        "pygame_enabled": os.getenv("RENDER") != "true",
    }

# ✅ NEW: RAINA CHAT ENDPOINT
@app.post("/api/raina_chat")
async def raina_chat(request: Request):
    """Simple chat endpoint that talks with the frontend."""
    try:
        data = await request.json()
        message = data.get("message", "").strip()

        if not message:
            return {"text": "Please say something, Red."}

        # Simple reply simulation
        reply = f"RAINA: I heard you say '{message}'. What would you like me to do next?"
        return {"text": reply}

    except Exception as e:
        return JSONResponse(content={"text": f"Error: {str(e)}"}, status_code=500)

# --- LOCAL RUNNER ---
if __name__ == "__main__":
    try:
        import uvicorn
        uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
    except Exception as e:
        print(f"❌ Failed to start app: {e}")
