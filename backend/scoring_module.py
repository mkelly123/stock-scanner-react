import pandas as pd

def score_row(latest: pd.Series) -> float:
    score = 0.0

    if latest["close"] > latest["ema_20"] > latest["sma_20"]:
        score += 2.0

    rsi = latest["rsi_14"]
    if 50 <= rsi <= 65:
        score += 1.5
    elif 40 <= rsi < 50 or 65 < rsi <= 70:
        score += 0.5

    if latest["macd_hist"] > 0:
        score += 1.0

    return score
