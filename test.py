import requests

res = requests.post(
    "http://127.0.0.1:5000/analyze",
    json={
        "ticker": "005930.KS",
        "buy_price": 70000,
        "stop_price": 65000
    }
)

print(res.json())
