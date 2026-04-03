# =========================
# pay.py (OXAPAY INVOICE VERSION)
# =========================

import requests
import json

API_KEY = "NLQIPG-8SOFHX-VPRQZ5-MQA7H9"


# 🔥 Create invoice (returns payment_url + track_id)
def create_payment(user_id: str):
    url = "https://api.oxapay.com/v1/payment/invoice"

    headers = {
        "merchant_api_key": API_KEY,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    data = {
        "amount": 1,  # ✅ low amount works
        "currency": "USD",
        "lifetime": 30,
        "fee_paid_by_payer": 1,
        "under_paid_coverage": 2,
        "to_currency": "USDT",
        "order_id": user_id,
        "description": f"User {user_id} payment",
        "sandbox": False
    }

    try:
        r = requests.post(url, data=json.dumps(data), headers=headers)

        print("STATUS:", r.status_code)
        print("RESPONSE:", r.text)

        res = r.json()

        if res.get("status") == 200:
            return res["data"]
        else:
            print("OxaPay Error:", res)
            return None

    except Exception as e:
        print("Error:", e)
        return None


# 🔥 Check payment status
def check_payment_status(track_id: str):
    url = "https://api.oxapay.com/v1/payment/inquiry"

    headers = {
        "merchant_api_key": API_KEY,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    data = {
        "track_id": track_id
    }

    try:
        r = requests.post(url, data=json.dumps(data), headers=headers)

        print("STATUS:", r.status_code)
        print("RESPONSE:", r.text)

        res = r.json()

        return res.get("data", {}).get("status")

    except Exception as e:
        print("Status error:", e)
        return None
