import os
import time
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from polygon import RESTClient

# Load API key
load_dotenv()
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

# Create Polygon client
client = RESTClient(api_key=POLYGON_API_KEY)

# ---------------------------------------------------------
# 1. Fetch intraday minute bars (correct ISO timestamps)
# ---------------------------------------------------------
def fetch_intraday(symbol: str) -> pd.DataFrame:
    """
    Fetch the last 5 minutes of 1‑minute bars from Polygon.
    Returns a pandas DataFrame with OHLCV.
    """
    try:
        now = datetime.utcnow()
        start = (now - timedelta(minutes=5)).isoformat()
        end = now.isoformat()

        bars = client.get_aggs(
            symbol,
            1,          # multiplier
            "minute",   # timespan
            start,
            end
        )

        rows = []
        for bar in bars:
            rows.append({
                "timestamp": bar.timestamp,
                "open": bar.open,
                "high": bar.high,
                "low": bar.low,
                "close": bar.close,
                "volume": bar.volume
            })

        df = pd.DataFrame(rows)

        if df.empty:
            print(f"[WARN] Polygon returned empty data for {symbol}")

        return df

    except Exception as e:
        print(f"[ERROR] Polygon fetch failed for {symbol}: {e}")
        return pd.DataFrame()


# ---------------------------------------------------------
# 2. Simple last‑trade fetch (fast, low‑rate‑limit)
# ---------------------------------------------------------
def fetch_polygon_agg(symbol: str):
    """
    Fetch the most recent trade (price + size).
    Much safer than minute aggregates for real‑time scanning.
    """
    try:
        trade = client.get_last_trade(symbol)

        return {
            "symbol": symbol,
            "price": trade.price,
            "volume": trade.size
        }

    except Exception as e:
        print(f"[ERROR] Polygon last trade failed for {symbol}: {e}")
        return None


# ---------------------------------------------------------
# 3. Cached tick fetch (recommended for scanner)
# ---------------------------------------------------------
TICK_CACHE = {}      # { symbol: { "ts": timestamp, "data": {...} } }
CACHE_TTL = 5        # seconds


def get_latest_tick(symbol: str):
    """
    Returns the latest tick for a symbol using:
    - cache (5 seconds)
    - Polygon last trade endpoint (fast, low cost)
    """
    try:
        now_ts = time.time()

        # 1. CACHE CHECK
        if symbol in TICK_CACHE:
            age = now_ts - TICK_CACHE[symbol]["ts"]
            if age < CACHE_TTL:
                return TICK_CACHE[symbol]["data"]

        # 2. FETCH FROM POLYGON (last trade)
        trade = client.get_last_trade(symbol)

        tick_data = {
            "symbol": symbol,
            "price": trade.price,
            "volume": trade.size
        }

        print(f"Polygon tick for {symbol}: price={trade.price}, volume={trade.size}")

        # 3. STORE IN CACHE
        TICK_CACHE[symbol] = {
            "ts": now_ts,
            "data": tick_data
        }

        return tick_data

    except Exception as e:
        print(f"[ERROR] Polygon fetch failed for {symbol}: {e}")
        return None
