import requests

API_KEY = "ACVHKoO2Lkhdk64f0khPqfCEt40RaJBw"
BASE = "https://api.massive.com/v2"

def get_batch_snapshots(symbols):
    """
    Fetch real-time snapshot data for multiple tickers in one request.
    """
    joined = ",".join(symbols)
    url = f"{BASE}/snapshot/locale/us/markets/stocks/tickers/{joined}"
    params = {"apiKey": API_KEY}

    try:
        r = requests.get(url, params=params)
        data = r.json()

        # Massive returns: { tickers: [ {...}, {...} ] }
        results = {}

        for item in data.get("tickers", []):
            symbol = item.get("ticker")
            results[symbol] = {
                "price": item.get("lastTrade", {}).get("p", 0),
                "volume": item.get("day", {}).get("v", 0),
                "changePct": item.get("todaysChangePerc", 0),
                "prevClose": item.get("prevDay", {}).get("c", 0),
            }

        return results

    except Exception as e:
        print(f"[BATCH SNAPSHOT ERROR] {e}")
        return {}

def get_batch_prevday(symbols):
    """
    Fetch previous-day aggregates for multiple tickers in one request.
    """
    joined = ",".join(symbols)
    url = f"{BASE}/aggs/ticker/{joined}/prev"
    params = {"apiKey": API_KEY}

    try:
        r = requests.get(url, params=params)
        data = r.json()

        # Massive returns: { results: [ {...}, {...} ] }
        results = {}

        for item in data.get("results", []):
            symbol = item.get("T")
            results[symbol] = {
                "volume": int(item.get("v", 1)),
                "open": item.get("o", 0),
                "close": item.get("c", 0),
                "high": item.get("h", 0),
                "low": item.get("l", 0),
                "vwap": item.get("vw", 0),
                "trades": item.get("n", 0),
                "timestamp": item.get("t", 0),
            }

        return results

    except Exception as e:
        print(f"[BATCH PREVDAY ERROR] {e}")
        return {}
