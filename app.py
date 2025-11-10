from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import stripe
import httpx
import os

app = FastAPI()

# Stripe secret key
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")  # or hardcode for now

# ✅ Checkout route
@app.get("/checkout")
def create_checkout(plan: str, email: str = "user@example.com"):
    session = stripe.checkout.Session.create(
        customer_email=email,
        line_items=[{"price": plan, "quantity": 1}],
        mode="subscription",
        success_url="https://botguard.redwineinnovations.com/success",
        cancel_url="https://botguard.redwineinnovations.com/cancel"
    )
    return RedirectResponse(session.url)

# ✅ Webhook route
@app.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except Exception as e:
        return {"error": str(e)}

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        email = session.get("customer_email")
        plan_id = session["display_items"][0]["price"]["id"]

        # 🔐 License activation via Make
        httpx.post("https://hook.us2.make.com/j2b7uw4kr4fajj85asstgcgd923c8mg7", json={
            "email": email,
            "plan": plan_id
        })

        # 📧 Brevo onboarding via Make
        httpx.post("https://hook.us2.make.com/s0ltqnyowhi7gkx242ttp8602957t79a", json={
            "email": email,
            "plan": plan_id
        })

    return {"status": "ok"}
