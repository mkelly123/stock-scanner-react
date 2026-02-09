import os
import time
import finnhub
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load API key
# Load .env from project root 
# Absolute path to project root 
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")) 
ENV_PATH = os.path.join(ROOT_DIR, ".env") 

print("DEBUG ENV PATH:", ENV_PATH) # should print C:\Dev\stock-scanner-react\.env 
load_dotenv(ENV_PATH) 

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY") 
print("DEBUG FINNHUB KEY:", FINNHUB_API_KEY)

# Create Finnhub client
client = finnhub.Client(api_key=FINNHUB_API_KEY)

# ---------------------------------------------------------
# Simple in‑memory cache
# ---------------------------------------------------------
TICK_CACHE = {}      # { symbol: { "ts": timestamp, "data": {...} } }
CACHE_TTL = 5        # seconds


def get_realtime_quote(symbol: str):
    try:
        now_ts = time.time()

        # Cache check
        if symbol in TICK_CACHE:
            age = now_ts - TICK_CACHE[symbol]["ts"]
            if age < CACHE_TTL:
                return TICK_CACHE[symbol]["data"]

        # Free-tier safe call
        quote = client.quote(symbol)

        tick_data = {
            "symbol": symbol,
            "price": quote.get("c"),
            "volume": quote.get("v"),        # Finnhub gives volume here
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

