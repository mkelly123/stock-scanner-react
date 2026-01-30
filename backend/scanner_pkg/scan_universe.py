from backend.data_providers.polygon_provider import get_latest_tick

def scan_universe(universe, filter_type="momentum"):
    results = []
    print("SCAN RESULTS:", results)
    for symbol in universe:
        tick = get_latest_tick(symbol)
        if not tick:
            continue

        # Basic real metrics
        rel_volume = tick["volume"] / 50_000_000
        change_pct = 0  # placeholder until you add real change logic

        row = {
            "symbol": tick["symbol"],
            "price": tick["price"],
            "volume": tick["volume"],
            "float": 0,
            "relVolume": rel_volume,
            "changePct": change_pct,
            "score": rel_volume * 10,
        }

        results.append(row)

    return results
