# filters.py

import pandas as pd

def momentum_filter(df: pd.DataFrame) -> bool: 
    """ 
    Basic momentum: price above EMA and EMA above SMA, 
    RSI not overbought, MACD positive. 
    """ 
    latest = df.iloc[-1] 
    
    price = latest["close"] 
    ema = latest["ema_20"] 
    sma = latest["sma_20"] 
    rsi = latest["rsi_14"] 
    macd_hist = latest["macd_hist"] 
    
    if pd.isna(ema) or pd.isna(sma) or pd.isna(rsi) or pd.isna(macd_hist): 
        return False 
    return ( 
        price > ema > sma and 
        40 < rsi < 70 and 
        macd_hist > 0 
    ) 

def breakout_filter(df: pd.DataFrame, lookback: int = 50) -> bool: 
    """ 
    Price making a new N-bar high with volume expansion. 
    """ 
    if len(df) < lookback + 1: 
        return False 
    
    recent = df.iloc[-lookback:] 
    latest = df.iloc[-1] 
    
    recent_high = recent["high"].max() 
    latest_close = latest["close"] 
    latest_vol = latest["volume"] 
    avg_vol = recent["volume"].mean() 
    
    return latest_close >= recent_high and latest_vol > 1.5 * avg_vol




















def passes_momentum_breakout_filters(df: pd.DataFrame, is_etf: bool = False) -> bool:
    if df.shape[0] < 200:
        return False

    latest = df.iloc[-1]

    price = latest["Close"]
    volume = latest["Volume"]
    sma50 = latest["sma50"]
    sma200 = latest["sma200"]
    atr14 = latest["atr14"]
    avg_volume_20 = latest["avg_volume_20"]
    highest_close_20 = latest["highest_close_20"]

    if pd.isna(sma50) or pd.isna(sma200) or pd.isna(atr14) or pd.isna(avg_volume_20) or pd.isna(highest_close_20):
        return False

    if is_etf:
        if not (5 <= price <= 200):
            return False
    else:
        if not (5 <= price <= 80):
            return False

    if avg_volume_20 <= (500_000 if is_etf else 1_000_000):
        return False

    if volume <= 1.5 * avg_volume_20:
        return False

    if not (price > sma50 > sma200):
        return False

    atr_percent = atr14 / price * 100
    if atr_percent <= (1.0 if is_etf else 2.0):
        return False

    pct_change_today = (latest["Close"] - latest["Open"]) / latest["Open"] * 100

    if latest["Close"] <= highest_close_20:
        return False

    if pct_change_today <= (2.0 if is_etf else 4.0):
        return False

    return True


def passes_breakout_high_gainer_filters(df: pd.DataFrame, float_value: int) -> bool:
    if df.shape[0] < 20:
        return False

    latest = df.iloc[-1]

    price = latest["Close"]
    volume = latest["Volume"]
    pct_change_today = (latest["Close"] - latest["Open"]) / latest["Open"] * 100
    highest_close_20 = df["highest_close_20"].iloc[-1]
    avg_volume_20 = df["avg_volume_20"].iloc[-1]
    rel_volume = volume / avg_volume_20 if avg_volume_20 else 0
    vwap = latest["vwap"]

    # Price range typical for low-float runners
    if not (1 <= price <= 20):
        return False

    # Volume sweet spot
    if not (50_000_000 <= volume <= 150_000_000):
        return False

    # Low float requirement
    if float_value >= 20_000_000:
        return False

    # Must be moving
    if pct_change_today < 5:
        return False

    # Relative volume confirmation
    if rel_volume < 3:
        return False

    # VWAP reclaim / hold
    if latest["Close"] < vwap:
        return False

    # Must be breaking out
    if latest["Close"] < highest_close_20:
        return False

    return True


def passes_multi_timeframe_confirmation(df_daily: pd.DataFrame, df_weekly: pd.DataFrame) -> bool:
    if df_daily.shape[0] < 20 or df_weekly.shape[0] < 50:
        return False

    daily_latest = df_daily.iloc[-1]
    weekly_latest = df_weekly.iloc[-1]

    daily_high_20 = df_daily["highest_close_20"].iloc[-1]
    weekly_sma50 = df_weekly["Close"].rolling(window=50).mean().iloc[-1]

    # Daily breakout
    if daily_latest["Close"] <= daily_high_20:
        return False

    # Weekly trend confirmation
    if weekly_latest["Close"] <= weekly_sma50:
        return False

    return True
