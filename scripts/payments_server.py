#!/usr/bin/env python3
"""
Minimal payments server using Stripe Checkout
- Provides /create-checkout-session to create hosted Checkout
- Optional /pay route to redirect for a given business name

Security notes:
- Never log raw secrets
- Use hosted Stripe Checkout (PCI compliant)
- Validate inputs and sanitize logs
"""

import os
import json
from flask import Flask, request, jsonify, redirect

app = Flask(__name__)

try:
    import stripe
except Exception:
    stripe = None

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_PRICE_ID = os.getenv("STRIPE_PRICE_ID", "")  # Pre-configured price ID for one-time payment
STRIPE_SUCCESS_URL = os.getenv("STRIPE_SUCCESS_URL", "http://localhost:5000/success")
STRIPE_CANCEL_URL = os.getenv("STRIPE_CANCEL_URL", "http://localhost:5000/cancel")

if stripe and STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY


def _safe(s: str, maxlen: int = 64) -> str:
    s = (s or "").strip()
    return s[:maxlen]


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    if not stripe:
        return jsonify({"error": "Stripe SDK not installed"}), 500
    if not STRIPE_SECRET_KEY:
        return jsonify({"error": "STRIPE_SECRET_KEY not configured"}), 500

    data = request.get_json(silent=True) or {}
    business = _safe(data.get("business", "Demo"))
    amount = int(data.get("amount", 0))

    try:
        if STRIPE_PRICE_ID:
            line_items = [{"price": STRIPE_PRICE_ID, "quantity": 1}]
        else:
            if amount <= 0:
                return jsonify({"error": "Specify positive amount or STRIPE_PRICE_ID"}), 400
            line_items = [{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": f"Deposit for {business}"},
                    "unit_amount": amount,
                },
                "quantity": 1,
            }]

        session = stripe.checkout.Session.create(
            mode="payment",
            line_items=line_items,
            success_url=STRIPE_SUCCESS_URL,
            cancel_url=STRIPE_CANCEL_URL,
            metadata={"business": business},
        )
        return jsonify({"url": session.url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/pay")
def pay():
    business = _safe(request.args.get("business", "Demo"))
    # Redirect to a created checkout session via client-side POST
    # Simple UX: instructs client to POST to /create-checkout-session
    html = f"""
    <html><body>
    <h3>Payment for {business}</h3>
    <form id="f" method="post" action="/create-checkout-session">
      <input type="hidden" name="business" value="{business}" />
      <input type="number" name="amount" placeholder="Amount (cents)" value="9900" />
      <button type="submit">Create Checkout</button>
    </form>
    <script>
    // Convert form post to JSON
    const f = document.getElementById('f');
    f.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(f);
      const payload = {};
      for (const [k,v] of formData.entries()) payload[k] = v;
      const res = await fetch('/create-checkout-session', {
        method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (data.url) window.location.href = data.url; else alert(data.error || 'Error');
    });
    </script>
    </body></html>
    """
    return html


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
