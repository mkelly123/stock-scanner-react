import requests
from backend.data_providers.cache import cache_get, cache_set

API_KEY = "ACVHKoO2Lkhdk64f0khPqfCEt40RaJBw"
BASE = "https://api.massive.com/v2"

def get_snapshot(symbol: str):
    print("[DEBUG SNAPSHOT]", symbol, data)

    cache_key = f"snapshot:{symbol}"
    cached = cache_get(cache_key)
    if cached:
        return cached

    url = f"{BASE}/snapshot/locale/us/markets/stocks/tickers/{symbol}"
    params = {"apiKey": API_KEY}

    try:
        r = requests.get(url, params=params)
        data = r.json()

        if "ticker" not in data:
            return {}

        t = data["ticker"]

        result = {
            "price": t.get("lastTrade", {}).get("p", 0),
            "volume": t.get("day", {}).get("v", 0),
            "changePct": t.get("todaysChangePerc", 0),
            "prevClose": t.get("prevDay", {}).get("c", 0),
        }

        cache_set(cache_key, result)
        return result

    except Exception as e:
        print(f"[MASSIVE SNAPSHOT ERROR] {symbol}: {e}")
        return {}
