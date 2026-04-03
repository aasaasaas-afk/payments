# =========================
# pay.py (OXAPAY WHITE-LABEL VERSION - BSC)
# =========================

import requests
import json

API_KEY = "NLQIPG-8SOFHX-VPRQZ5-MQA7H9"


# 🔥 Create payment (returns wallet address)
def create_payment(user_id: str):
    url = "https://api.oxapay.com/v1/payment/white-label"

    headers = {
        "merchant_api_key": API_KEY,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    data = {
        "amount": 10,                     # ✅ $1
        "currency": "USD",
        "pay_currency": "USDT",          # receive in USDT
        "network": "BSC",                # ✅ BSC (BEP20)
        "lifetime": 30,
        "fee_paid_by_payer": 1,
        "under_paid_coverage": 2,
        "to_currency": "USDT",
        "order_id": user_id,
        "description": f"User {user_id} payment",
        "callback_url": "https://yourdomain.com/callback"
    }

    try:
        r = requests.post(url, data=json.dumps(data), headers=headers)

        print("STATUS:", r.status_code)
        print("RESPONSE:", r.text)

        res = r.json()

        if res.get("status") == 200:
            data = res["data"]

            return {
                "track_id": data["track_id"],
                "address": data["address"],
                "amount": data["pay_amount"],
                "currency": data["pay_currency"],
                "network": data["network"],
                "qr": data["qr_code"],
                "expires": data["expired_at"]
            }
        else:
            print("OxaPay Error:", res)
            return None

    except Exception as e:
        print("Error:", e)
        return None


# 🔥 Check payment status (FIXED ENDPOINT)
def check_payment_status(track_id: str):
    url = f"https://api.oxapay.com/v1/payment/{track_id}"

    headers = {
        "merchant_api_key": API_KEY,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = requests.get(url, headers=headers)

        print("STATUS:", r.status_code)
        print("RESPONSE:", r.text)

        res = r.json()

        return res.get("data", {}).get("status")

    except Exception as e:
        print("Status error:", e)
        return None
