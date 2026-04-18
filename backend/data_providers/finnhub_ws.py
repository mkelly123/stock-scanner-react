import os
import finnhub
from datetime import datetime, timedelta

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

client = finnhub.Client(api_key=FINNHUB_API_KEY)

def get_company_news(symbol: str):
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=7)

    news = client.company_news(
        symbol,
        _from=str(week_ago),
        to=str(today)
    )

    return [
        {
            "symbol": symbol.upper(),
            "headline": item.get("headline", ""),
            "source": item.get("source", ""),
            "summary": item.get("summary", ""),
            "url": item.get("url", ""),
            "timestamp": item.get("datetime", 0)
        }
        for item in news
    ]

def get_realtime_quote(symbol: str):
    """
    Returns a dict with:
    - price
    - volume
    - prev_close
    - avg_volume (fallback to volume)
    """

    try:
        q = client.quote(symbol)

        return {
            "price": q.get("c"),          # current price
            "prev_close": q.get("pc"),    # previous close
            "volume": q.get("v"),         # volume today
            "avg_volume": q.get("v"),     # Finnhub free tier doesn't give avgVol
        }

    except Exception as e:
        print(f"[FINNHUB ERROR] {symbol}: {e}")
        return None
