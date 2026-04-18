import os
import time
import finnhub
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load API key
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ENV_PATH = os.path.join(ROOT_DIR, ".env")

print("DEBUG ENV PATH:", ENV_PATH)
load_dotenv(ENV_PATH)

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
print("DEBUG FINNHUB KEY:", FINNHUB_API_KEY)

# Create Finnhub client
client = finnhub.Client(api_key=FINNHUB_API_KEY)

# ---------------------------------------------------------
# Simple in‑memory cache
# ---------------------------------------------------------
TICK_CACHE = {}
CACHE_TTL = 5  # seconds


def get_realtime_quote(symbol: str):
    try:
        now_ts = time.time()

        # Cache check
        if symbol in TICK_CACHE:
            age = now_ts - TICK_CACHE[symbol]["ts"]
            if age < CACHE_TTL:
                return TICK_CACHE[symbol]["data"]

        quote = client.quote(symbol)

        tick_data = {
            "symbol": symbol,
            "price": quote.get("c"),
            "volume": quote.get("v"),
            "changePct": quote.get("dp"),
            "prevClose": quote.get("pc"),
        }

        TICK_CACHE[symbol] = {
            "ts": now_ts,
            "data": tick_data
        }

        return tick_data

    except Exception as e:
        print(f"[ERROR] Finnhub fetch failed for {symbol}: {e}")
        return None


# ---------------------------------------------------------
# NEWS PROVIDER (with fallback)
# ---------------------------------------------------------
def get_company_news(symbol: str):
    """
    Fetches company news for the last 7 days.
    If empty, falls back to general market news.
    Always returns a list of dicts.
    """
    try:
        today = datetime.utcnow().date()
        week_ago = today - timedelta(days=7)

        # Try company-specific news
        news = client.company_news(
            symbol,
            _from=str(week_ago),
            to=str(today)
        )

        print(">>> COMPANY NEWS COUNT:", len(news))

        if news:
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

        # Fallback: general market news
        print(">>> USING GENERAL NEWS FALLBACK")
        general = client.general_news("general", min_id=0)

        return [
            {
                "symbol": symbol.upper(),
                "headline": item.get("headline", ""),
                "source": item.get("source", ""),
                "summary": item.get("summary", ""),
                "url": item.get("url", ""),
                "timestamp": item.get("datetime", 0)
            }
            for item in general[:10]
        ]

    except Exception as e:
        print(f"[ERROR] Finnhub news fetch failed for {symbol}: {e}")
        return []
