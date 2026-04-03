# =========================
# pay.py (OXAPAY VERSION)
# =========================

import requests

API_KEY = "ZRDRKF-PQLS5Q-BVYUXM-JI5QPZ"


# 🔥 Create payment (returns address + amount + trackId)
def create_payment(user_id: str, network: str):
    url = "https://api.oxapay.com/v1/payment"

    data = {
        "merchant": API_KEY,
        "amount": 1,  # ✅ you can keep low amount here (1–5 works)
        "currency": "USD",
        "lifeTime": 30,
        "feePaidByPayer": 1,
        "underPaidCover": 2,
        "description": f"User {user_id} payment"
    }

    # 🔥 Network handling
    if network == "trc20":
        data["network"] = "TRC20"
        data["currency"] = "USDT"
    elif network == "bep20":
        data["network"] = "BEP20"
        data["currency"] = "USDT"

    try:
        r = requests.post(url, json=data)

        print("STATUS CODE:", r.status_code)
        print("RESPONSE:", r.text)

        res = r.json()

        # ✅ success check
        if res.get("result") == 100:
            return res
        else:
            print("OxaPay Error:", res)
            return None

    except Exception as e:
        print("Payment creation error:", e)
        return None


# 🔥 Check payment status
def check_payment_status(track_id: str):
    url = "https://api.oxapay.com/v1/payment/inquiry"

    data = {
        "merchant": API_KEY,
        "trackId": track_id
    }

    try:
        r = requests.post(url, json=data)

        print("STATUS CODE:", r.status_code)
        print("RESPONSE:", r.text)

        res = r.json()

        return res.get("status")  # 100 = paid

    except Exception as e:
        print("Status error:", e)
        return None
