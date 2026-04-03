# =========================
# pay.py (COINREMITTER VERSION)
# =========================

import requests

API_KEY = "wkey_41XKWEJ1jeP8OG9"
PASSWORD = "Rocky@2009"

BASE_URL = "https://coinremitter.com/api/v3/usdt"


# 🔥 Generate new address
def create_payment(user_id: str):
    url = f"{BASE_URL}/get-new-address"

    data = {
        "api_key": API_KEY,
        "password": PASSWORD,
        "label": f"user_{user_id}"
    }

    try:
        r = requests.post(url, data=data)
        res = r.json()

        print("CREATE RESPONSE:", res)

        if res.get("flag") == 1:
            return res["data"]["address"]
        else:
            return None

    except Exception as e:
        print("Error:", e)
        return None


# 🔥 Check balance
def check_payment_status(address: str):
    url = f"{BASE_URL}/get-address-balance"

    data = {
        "api_key": API_KEY,
        "password": PASSWORD,
        "address": address
    }

    try:
        r = requests.post(url, data=data)
        res = r.json()

        print("BALANCE RESPONSE:", res)

        if res.get("flag") == 1:
            return float(res["data"]["balance"])
        else:
            return 0

    except Exception as e:
        print("Error:", e)
        return 0
