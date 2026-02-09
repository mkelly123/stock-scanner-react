import requests

def get_top_gainers(limit=20):
    url = "https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved"
    params = {"formatted": "false", "scrIds": "day_gainers"}
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    }

    try:
        resp = requests.get(url, params=params, headers=headers)
        text = resp.text

        # Debug
        print("RAW RESPONSE:", text[:200])

        data = resp.json()

        result = data.get("finance", {}).get("result", [])
        if not result:
            print("No result[] in response")
            return []

        quotes = result[0].get("quotes", [])
        if not quotes:
            print("No quotes[] in response")
            return []

        symbols = [q["symbol"] for q in quotes[:limit]]
        return symbols

    except Exception as e:
        print("Error fetching top gainers:", e)
        return []
