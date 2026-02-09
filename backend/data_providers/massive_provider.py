import requests
from backend.data_providers.cache import cache_get, cache_set

API_KEY = "ACVHKoO2Lkhdk64f0khPqfCEt40RaJBw"
BASE = "https://api.massive.com/v2"

def get_prev_day_agg(symbol: str):
    cache_key = f"prevday:{symbol}"
    cached = cache_get(cache_key)
    if cached:
        return cached

    url = f"{BASE}/aggs/ticker/{symbol}/prev"
    params = {"apiKey": API_KEY}

    try:
        r = requests.get(url, params=params)
        data = r.json()

        if data.get("status") == "OK" and data.get("results"):
            result = data["results"][0]

            parsed = {
                "volume": int(result.get("v", 1)),
                "open": result.get("o", 0),
                "close": result.get("c", 0),
                "high": result.get("h", 0),
                "low": result.get("l", 0),
                "vwap": result.get("vw", 0),
                "trades": result.get("n", 0),
                "timestamp": result.get("t", 0),
            }

            cache_set(cache_key, parsed)
            return parsed

    except Exception as e:
        print(f"[MASSIVE PROVIDER ERROR] {symbol}: {e}")

    return {"volume": 1}
