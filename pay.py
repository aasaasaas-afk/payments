# =========================
# pay.py (COINREMITTER V1 FIXED)
# =========================

import requests

API_KEY = "wkey_41XKWEJ1jeP8OG9"
API_PASSWORD = "Rocky@2009"

BASE_URL = "https://api.coinremitter.com/v1"


# 🔥 Create new address
def create_payment(user_id: str):
    url = f"{BASE_URL}/wallet/address/create"

    headers = {
        "x-api-key": API_KEY,
        "x-api-password": API_PASSWORD,
        "Content-Type": "application/json"
    }

    data = {
        "label": f"user_{user_id}"[:20]  # max 20 chars
    }

    try:
        r = requests.post(url, json=data, headers=headers)

        print("STATUS:", r.status_code)
        print("RAW RESPONSE:", r.text)

        res = r.json()

        if res.get("success"):
            return res["data"]["address"]
        else:
            print("API ERROR:", res)
            return None

    except Exception as e:
        print("Error:", e)
        return None


# 🔥 Check transactions (IMPORTANT CHANGE)
def check_payment_status(address: str):
    url = f"{BASE_URL}/wallet/address/transactions"

    headers = {
        "x-api-key": API_KEY,
        "x-api-password": API_PASSWORD,
        "Content-Type": "application/json"
    }

    data = {
        "address": address
    }

    try:
        r = requests.post(url, json=data, headers=headers)

        print("STATUS:", r.status_code)
        print("RAW RESPONSE:", r.text)

        res = r.json()

        if not res.get("success"):
            return 0

        confirm_amount = float(res["data"]["confirm_amount"])
        return confirm_amount

    except Exception as e:
        print("Error:", e)
        return 0
