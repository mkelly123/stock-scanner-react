# indicators.py

import pandas as pd
import numpy as np

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Assumes df has: timestamp, open, high, low, close, volume
    Adds: sma_20, ema_20, vwap, rsi_14, macd, macd_signal, macd_hist
    """

    # Simple Moving Average
    df["sma_20"] = df["close"].rolling(20).mean()

    # Exponential Moving Average
    df["ema_20"] = df["close"].ewm(span=20, adjust=False).mean()

    # VWAP
    typical_price = (df["high"] + df["low"] + df["close"]) / 3
    df["vwap"] = (typical_price * df["volume"]).cumsum() / df["volume"].cumsum()

    # RSI 14
    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    df["rsi_14"] = 100 - (100 / (1 + rs))

    # MACD (12, 26, 9)
    ema12 = df["close"].ewm(span=12, adjust=False).mean()
    ema26 = df["close"].ewm(span=26, adjust=False).mean()
    df["macd"] = ema12 - ema26
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()
    df["macd_hist"] = df["macd"] - df["macd_signal"]

    return df
































# import pandas as pd


# def add_vwap(df: pd.DataFrame) -> pd.DataFrame:
#     df = df.copy()
#     typical_price = (df["High"] + df["Low"] + df["Close"]) / 3
#     df["vwap"] = (typical_price * df["Volume"]).cumsum() / df["Volume"].cumsum()
#     return df


# def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
#     df = df.copy()

#     df["sma50"] = df["Close"].rolling(window=50).mean()
#     df["sma200"] = df["Close"].rolling(window=200).mean()

#     df["prev_close"] = df["Close"].shift(1)
#     df["tr1"] = df["High"] - df["Low"]
#     df["tr2"] = (df["High"] - df["prev_close"]).abs()
#     df["tr3"] = (df["Low"] - df["prev_close"]).abs()
#     df["true_range"] = df[["tr1", "tr2", "tr3"]].max(axis=1)
#     df["atr14"] = df["true_range"].rolling(window=14).mean()

#     df["avg_volume_20"] = df["Volume"].rolling(window=20).mean()
#     df["highest_close_20"] = df["Close"].rolling(window=20).max()

#     df = add_vwap(df)

#     return df
