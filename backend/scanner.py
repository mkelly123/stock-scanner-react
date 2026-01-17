# scanner.py

import yfinance as yf
import pandas as pd
import time
from typing import List, Dict
from pathlib import Path
from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# =========================
# MODEL
# =========================

class ScanResult(BaseModel):
    symbol: str
    price: float
    volume: int
    float: int
    relVolume: float
    changePct: float

# =========================
# STATIC ENDPOINT (for now)
# =========================

@router.get("/scan", response_model=List[ScanResult])
def get_scan_results():
    return [
        {"symbol": "BACK", "price": 6.35, "volume": 485590, "float": 1020000, "relVolume": 3.35, "changePct": 82.21},
        {"symbol": "BRFH", "price": 1.52, "volume": 39800000, "float": 6890000, "relVolume": 8598.03, "changePct": 47.57},
        {"symbol": "PCSA", "price": 2.38, "volume": 67680000, "float": 2230000, "relVolume": 273.83, "changePct": 47.22},
        {"symbol": "MNY",  "price": 2.42, "volume": 6870000,  "float": 13820000, "relVolume": 34.34, "changePct": 34.44},
        {"symbol": "YYGH", "price": 2.94, "volume": 18040000, "float": 34800000, "relVolume": 41.26, "changePct": 30.08},
        {"symbol": "POAI", "price": 1.72, "volume": 157690,  "float": 3920000,  "relVolume": 5.0,  "changePct": 28.33},
    ]

# =========================
# CONFIG
# =========================

STOCK_UNIVERSE = ["AAPL", "MSFT", "NVDA", "AMZN", "META"]
ETF_UNIVERSE = ["SPY", "QQQ", "VUKG"]

SLEEP_SECONDS = 1 # polite delay between requests
RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

# =========================
# INDICATORS
# =========================

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["sma50"] = df["Close"].rolling(window=50).mean()
    df["sma200"] = df["Close"].rolling(window=200).mean()

    df["prev_close"] = df["Close"].shift(1)
    df["tr1"] = df["High"] - df["Low"]
    df["tr2"] = (df["High"] - df["prev_close"]).abs()
    df["tr3"] = (df["Low"] - df["prev_close"]).abs()
    df["true_range"] = df[["tr1", "tr2", "tr3"]].max(axis=1)
    df["atr14"] = df["true_range"].rolling(window=14).mean()

    df["avg_volume_20"] = df["Volume"].rolling(window=20).mean()
    df["highest_close_20"] = df["Close"].rolling(window=20).max()

    return df

# =========================
# FILTERS & SCORING
# =========================

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

    # Slightly looser bounds for ETFs
    if is_etf:
        if not (5 <= price <= 200):
            return False
    else:
        if not (5 <= price <= 80):
            return False

    if avg_volume_20 <= 500_000 if is_etf else avg_volume_20 <= 1_000_000:
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

def compute_score(df: pd.DataFrame) -> float:
    latest = df.iloc[-1]

    price = latest["Close"]
    sma50 = latest["sma50"]
    volume = latest["Volume"]
    avg_volume_20 = latest["avg_volume_20"]
    atr14 = latest["atr14"]

    pct_change_today = (latest["Close"] - latest["Open"]) / latest["Open"] * 100
    trend_strength = (price - sma50) / sma50 * 100 if sma50 else 0
    volume_surge = volume / avg_volume_20 if avg_volume_20 else 0
    atr_percent = atr14 / price * 100 if price else 0

    score = (
        0.4 * pct_change_today +
        0.3 * trend_strength +
        0.2 * volume_surge +
        0.1 * atr_percent
    )

    return score

# =========================
# SCANNER
# =========================

def scan_universe(universe: List[str], mode: str = "stocks") -> List[Dict]:
    results = []
    is_etf_mode = (mode == "etf")

    for i, symbol in enumerate(universe, start=1):
        print(f"[{i}/{len(universe)}] Scanning {symbol}...")

        try:
            df = yf.download(symbol, period="1y", interval="1d", progress=False)
        except Exception as e:
            print(f"[ERROR] Failed to fetch {symbol}: {e}")
            continue

        if df.empty:
            print(f"[WARN] No data for {symbol}")
            continue

        # Flatten MultiIndex columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = add_indicators(df)

        if not passes_momentum_breakout_filters(df, is_etf=is_etf_mode):
            continue

        score = compute_score(df)
        latest = df.iloc[-1]

        results.append({
            "symbol": symbol,
            "date": latest.name.strftime("%Y-%m-%d"),
            "price": round(latest["Close"], 2),
            "pct_change": round((latest["Close"] - latest["Open"]) / latest["Open"] * 100, 2),
            "volume": int(latest["Volume"]),
            "score": round(score, 2),
            "mode": mode,
        })

        time.sleep(SLEEP_SECONDS)

    results.sort(key=lambda x: x["score"], reverse=True)
    return results

def save_results(candidates: List[Dict], mode: str) -> None:
    if not candidates:
        return
    df = pd.DataFrame(candidates)
    today = datetime.now().strftime("%Y-%m-%d")
    path = RESULTS_DIR / f"{today}_scan_{mode}.csv"
    df.to_csv(path, index=False)
    print(f"\n[INFO] Saved results to {path}")
