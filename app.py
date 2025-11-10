import os
import time
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import Stripe safely
import stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Disable pygame on Render (no GUI/audio)
if os.getenv("RENDER") != "true":
    try:
        import pygame
        pygame.init()
        print("Pygame initialized locally.")
    except Exception as e:
        print("Pygame failed to init:", e)
else:
    print("Running on Render: pygame disabled.")

# Initialize FastAPI
app = FastAPI(title="RAINA LiveBuild API", version="2.0")

# --- ROUTES ---

@app.get("/")
def root():
    return {"status": "Online ✅", "service": "RAINA + Stripe Integration"}

@app.get("/api/stripe/test")
def stripe_test():
    """Check Stripe connection and list available balance if key valid."""
    try:
        balance = stripe.Balance.retrieve()
        return {"status": "Connected ✅", "available": balance.get("available")}
    except Exception as e:
        return JSONResponse(content={"status": "Error ❌", "detail": str(e)}, status_code=500)

@app.get("/api/status")
def status():
    """Basic heartbeat check."""
    return {"raina": "active", "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}

@app.get("/api/info")
def info():
    """System info."""
    return {
        "environment": "Render" if os.getenv("RENDER") == "true" else "Local",
        "stripe_key_set": bool(os.getenv("STRIPE_SECRET_KEY")),
        "pygame_enabled": os.getenv("RENDER") != "true",
    }

# --- RUN LOCAL ---
if __name__ == "__main__":
    try:
        import uvicorn
        uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
    except Exception as e:
        print(f"Failed to start app: {e}")
