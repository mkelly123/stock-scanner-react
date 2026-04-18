import time
from data_providers.yahoo_provider import get_quote_and_float

def scan_universe(universe, filter_type=None):
    symbols = universe
    results = []

    for symbol in symbols:
        data = get_quote_and_float(symbol)

        if not data:
            continue

        price = data["price"]
        volume = data["volume"]
        prev_close = data["prev_close"] or 0
        avg_volume = data["avg_volume"] or 1
        float_shares = data["float_shares"] or None

        # --- RELATIVE VOLUME ---
        rel_vol = volume / avg_volume if avg_volume else 1.0

        # --- SCORE ---
        score = (rel_vol * 0.6) + ((price - prev_close) / prev_close * 100 * 0.3 if prev_close else 0) + (volume * 0.1)

        results.append({
            "symbol": symbol,
            "price": price,
            "changePct": ((price - prev_close) / prev_close * 100) if prev_close else 0,
            "volume": volume,
            "relVolume": rel_vol,
            "score": score,
            "prevClose": prev_close,
            "float": float_shares,
        })

        time.sleep(0.05)

    return results
