import time
from backend.data_providers.finnhub_snapshot import get_realtime
from backend.data_providers.massive_provider import get_prev_day_agg

print(">>> ACTIVE scan_universe FILE:", __file__)



def scan_universe(universe, filter_type=None, strategy="swing"):
    print(">>> ENTERED scan_universe()")

    symbols = universe
    results = []

    for symbol in symbols:
        print(">>> ENTERING LOOP FOR:", symbol)        

        # --- REALTIME DATA (Finnhub) ---
        try:
            rt = get_realtime(symbol) or {}
        except Exception as e:
            print(f"[REALTIME ERROR] {symbol}: {e}")
            rt = {}

        price = rt.get("price", 0)
        change_pct = rt.get("changePct", 0)
        volume = rt.get("volume", 0)
        prev_close = rt.get("prevClose", 0)

        # --- PREVIOUS DAY DATA (replaced Massive.com) ---
        # Use Finnhub's prevClose and today's volume as proxy
        avg_volume = volume if volume > 0 else 1

        # --- RELATIVE VOLUME ---
        rel_vol = volume / avg_volume if avg_volume else 1.0

        # Trend classification
        if price > prev_close * 1.005:
            trend = "uptrend"
        elif price < prev_close * 0.995:
            trend = "downtrend"
        else:
            trend = "chop"


        # Gap detection
        if prev_close > 0:
            gap_pct = (price - prev_close) / prev_close * 100
        else:
            gap_pct = 0

        gap_up = gap_pct > 1.0      # > 1% gap up
        gap_down = gap_pct < -1.0   # > 1% gap down


        # Volatility proxy (ATR-style)
        volatility = abs(change_pct) * rel_vol



        # ---------------------------------------------------------
        # STRATEGY LOGIC
        # ---------------------------------------------------------

        # =========================================================
        # INTRADAY STRATEGY
        # =========================================================
        if strategy == "intraday":

            # Big % movers
            big_move = change_pct > 2

            # High relative volume
            high_rel_vol = rel_vol > 1.5

            # Clean trend proxy: price > prev close
            clean_trend = price > prev_close

            # Volatility filter: avoid dead stocks
            volatile_enough = volatility > 1.5

            intraday_score = (
                (2 if big_move else 0) +
                (2 if high_rel_vol else 0) +
                (1 if clean_trend else 0) +
                (1 if volatile_enough else 0) +
                (1 if gap_up else 0)   # gap up continuation
            )

            combined_score = (
                intraday_score * 0.7 +
                rel_vol * 0.2 +
                volatility * 0.1
            )


            results.append({
                "symbol": symbol,
                "price": price,
                "changePct": change_pct,
                "volume": volume,
                "relVolume": rel_vol,
                "intradayScore": intraday_score,
                "bigMove": big_move,
                "highRelVol": high_rel_vol,
                "cleanTrend": clean_trend,
                "trend": trend,
                "gapPct": gap_pct,
                "gapUp": gap_up,
                "gapDown": gap_down,
                "volatility": volatility,
                "combinedScore": combined_score,
                "strategy": "intraday"
            })

        # =========================================================
        # SWING STRATEGY
        # =========================================================
        else:

            # Trend proxy: today > yesterday
            trend_up = price > prev_close

            # Pullback: price dipped but still in trend
            pullback = trend_up and (abs(price - prev_close) / prev_close) < 0.03

            # Breakout proxy: strong % move
            breakout = change_pct > 1.5

            # Liquidity
            liquid = avg_volume > 300_000

            # Avoid low-volatility chop
            volatile_enough = volatility > 0.5

            swing_score = (
                (2 if trend_up else 0) +
                (2 if breakout else 0) +
                (2 if pullback else 0) +
                (2 if liquid else 0) +
                (1 if volatile_enough else 0) +
                (1 if gap_up else 0)   # breakout continuation
            )

            combined_score = (
                swing_score * 0.6 +
                rel_vol * 0.2 +
                volatility * 0.2
            )


            results.append({
                "symbol": symbol,
                "price": price,
                "changePct": change_pct,
                "volume": volume,
                "relVolume": rel_vol,
                "swingScore": swing_score,
                "trendUp": trend_up,
                "breakout": breakout,
                "liquid": liquid,
                "trend": trend,
                "gapPct": gap_pct,
                "gapUp": gap_up,
                "gapDown": gap_down,
                "volatility": volatility,
                "combinedScore": combined_score,
                "strategy": "swing"
            })

        time.sleep(0.05)

        # Sort results by score depending on strategy
        if strategy == "intraday":
            results.sort(key=lambda x: x.get("intradayScore", 0), reverse=True)
        else:
            results.sort(key=lambda x: x.get("swingScore", 0), reverse=True)

        results.sort(key=lambda x: x.get("combinedScore", 0), reverse=True)

    print(">>> ABOUT TO RETURN RESULTS:", results)

    return results

