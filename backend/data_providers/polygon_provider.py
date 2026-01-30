import os
import pandas as pd
import time
from dotenv import load_dotenv
from polygon import RESTClient
from datetime import datetime, timedelta

load_dotenv()
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

client = RESTClient(POLYGON_API_KEY)

def fetch_intraday(symbol: str) -> pd.DataFrame:
    """
    Fetch 1‑minute intraday bars from Polygon (last ~500 minutes).
    Returns a clean pandas DataFrame with OHLCV.
    """

    try:
        # Compute date range for last 500 minutes
        end = datetime.utcnow()
        start = end - timedelta(minutes=500)

        # Polygon requires ISO8601 strings
        start_str = start.strftime("%Y-%m-%d")
        end_str = end.strftime("%Y-%m-%d")

        # ⭐ Correct positional API call
        bars = client.get_aggs(
            symbol,        # ticker
            1,             # multiplier
            "minute",      # timespan
            start_str,     # from
            end_str        # to
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



def fetch_polygon_agg(symbol: str): 
    try: 
        # Example: last 1 minute of data 
        aggs = client.get_aggs( 
            symbol, 
            1, 
            "minute", 
            "2024-01-01", 
            "2024-01-01" 
        ) 
        
        if len(aggs) == 0: 
            raise Exception("No data returned") 
        
        bar = aggs[0] 
        
        return { 
            "symbol": symbol, 
            "price": bar.close, 
            "volume": bar.volume, 
        } 
    except Exception as e: 
        print(f"[ERROR] Polygon fetch failed for {symbol}: {e}") 
        return None


# Simple in‑memory cache 
TICK_CACHE = {} # { symbol: { "ts": timestamp, "data": {...} } } 
CACHE_TTL = 5 # seconds 

def get_latest_tick(symbol: str): 
    try: 
        now_ts = time.time() 
        # ----------------------------- 
        # 1. CACHE CHECK 
        # ----------------------------- 
        if symbol in TICK_CACHE: 
            age = now_ts - TICK_CACHE[symbol]["ts"] 
            if age < CACHE_TTL: 
                return TICK_CACHE[symbol]["data"] 
            
        # ----------------------------- 
        # 2. FETCH FROM POLYGON 
        # ----------------------------- 
        now = datetime.utcnow() 
        start = (now - timedelta(minutes=5)).strftime("%Y-%m-%d") 
        end = now.strftime("%Y-%m-%d") 
        
        bars = client.get_aggs(symbol, 1, "minute", start, end) 
        
        if not bars or len(bars) == 0: 
            print(f"[WARN] No bars returned for {symbol}") 
            return None 
        latest = bars[-1] 
        
        # Validate expected fields 
        if not hasattr(latest, "close") or not hasattr(latest, "volume"): 
            print(f"[WARN] Missing fields in latest bar for {symbol}: {latest}") 
            return None 
        
        tick_data = { 
            "symbol": symbol, 
            "price": latest.close, 
            "volume": latest.volume 
        } 
        
        print(f"Polygon tick for {symbol}: close={latest.close}, volume={latest.volume}") 
        
        # ----------------------------- 
        # 3. STORE IN CACHE 
        # ----------------------------- 
        TICK_CACHE[symbol] = { 
            "ts": now_ts, 
            "data": tick_data 
        } 
        return tick_data 
    except Exception as e: 
        print(f"[ERROR] Polygon fetch failed for {symbol}: {e}") 
        return None
