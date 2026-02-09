import requests

FINNHUB_KEY = "d6537c1r01qqbln5n0tgd6537c1r01qqbln5n0u0"
BASE = "https://finnhub.io/api/v1"

def get_realtime(symbol: str):
    """
    Fetch real-time price, volume, and change % from Finnhub.
    """
    url = f"{BASE}/quote"
    params = {"symbol": symbol, "token": FINNHUB_KEY}

    try:
        r = requests.get(url, params=params)
        data = r.json()

        return {
            "price": data.get("c", 0),
            "prevClose": data.get("pc", 0),
            "changePct": data.get("dp", 0),
            "volume": data.get("v", 0),
        }

    except Exception as e:
        print(f"[FINNHUB ERROR] {symbol}: {e}")
        return {}
