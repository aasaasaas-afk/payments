# =========================
# pay.py (UPDATED FOR /v1/payment API - IN-BOT ADDRESS FLOW)
# =========================

import requests

API_KEY = "HHQWVKJ-SV2MDEH-QG6KGZQ-B2JM7YT"

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}


# Create payment (returns address + amount)
def create_payment(user_id: str, pay_currency: str):
    url = "https://api.nowpayments.io/v1/payment"

    data = {
        "price_amount": 10,
        "price_currency": "usd",
        "pay_currency": pay_currency,
        "order_id": user_id,
        "order_description": "Test Payment $1"
    }

    try:
        r = requests.post(url, json=data, headers=HEADERS)

        print("STATUS CODE:", r.status_code)
        print("RESPONSE:", r.text)  # 🔥 IMPORTANT

        return r.json()

    except Exception as e:
        print("Payment creation error:", e)
        return None


# Check payment status
def check_payment_status(payment_id: str):
    url = f"https://api.nowpayments.io/v1/payment/{payment_id}"

    try:
        r = requests.get(url, headers=HEADERS)
        data = r.json()

        return data.get("payment_status")

    except Exception as e:
        print("Status error:", e)
        return None
