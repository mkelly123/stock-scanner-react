# utils_float.py

import yfinance as yf


def get_float(symbol: str) -> int:
    """
    Fetch float shares using yfinance.
    Falls back gracefully if data is missing.
    """
    try:
        ticker = yf.Ticker(symbol)

        # fast_info is quicker and more reliable
        info = ticker.fast_info

        for key in ["float_shares", "shares_float", "implied_shares_outstanding"]:
            if hasattr(info, key):
                value = getattr(info, key)
                if value not in (None, 0):
                    return int(value)

        # fallback to slower .info
        info = ticker.info
        for key in ["floatShares", "sharesFloat", "impliedSharesOutstanding"]:
            if key in info and info[key] not in (None, 0):
                return int(info[key])

    except Exception as e:
        print(f"[WARN] Failed to fetch float for {symbol}: {e}")

    return 0
