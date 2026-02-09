import yfinance as yf

def get_quote_and_float(symbol: str) -> dict | None:
    try:
        ticker = yf.Ticker(symbol)

        fast = ticker.fast_info
        info = ticker.get_info()  # slower, but fine for float

        price = fast.last_price
        volume = fast.last_volume
        prev_close = fast.previous_close
        avg_volume = fast.get("ten_day_average_volume") or fast.get("three_month_average_volume")

        float_shares = info.get("floatShares") or info.get("sharesOutstanding")

        if price is None or volume is None:
            return None

        return {
            "symbol": symbol,
            "price": float(price),
            "volume": int(volume),
            "prev_close": float(prev_close) if prev_close else None,
            "avg_volume": int(avg_volume) if avg_volume else None,
            "float_shares": int(float_shares) if float_shares else None,
        }

    except Exception as e:
        print(f"[YAHOO] Error for {symbol}: {e}")
        return None
