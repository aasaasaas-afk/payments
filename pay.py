import requests

API_KEY = "HHQWVKJ-SV2MDEH-QG6KGZQ-B2JM7YT"

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}


def create_invoice(user_id: str):
    url = "https://api.nowpayments.io/v1/invoice"

    data = {
        "price_amount": 1,
        "price_currency": "usd",
        "order_id": user_id,
        "order_description": "Test Payment $1"
    }

    try:
        r = requests.post(url, json=data, headers=HEADERS)
        return r.json()
    except Exception as e:
        print("Invoice error:", e)
        return None


def check_payment_status(payment_id: str):
    url = f"https://api.nowpayments.io/v1/invoice/{payment_id}"

    try:
        r = requests.get(url, headers=HEADERS)
        data = r.json()

        payments = data.get("payments", [])

        if not payments:
            return "waiting"

        return payments[-1].get("payment_status")

    except Exception as e:
        print("Status error:", e)
        return None
