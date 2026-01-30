from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import yfinance as yf
print("Importing news.py...")

router = APIRouter()

class NewsItem(BaseModel):
    symbol: str
    headline: str
    source: str
    timestamp: int
    url: str

def get_news_sentiment(symbol: str):
    # placeholder logic — replace with your real sentiment code
    return {"symbol": symbol, "sentiment": "neutral"}

@router.get("/news/{symbol}", response_model=List[NewsItem])
def get_news(symbol: str):
    ticker = yf.Ticker(symbol)
    raw_news = ticker.news or []

    return [
        {
            "symbol": symbol.upper(),
            "headline": item.get("title", ""),
            "source": item.get("publisher", ""),
            "timestamp": item.get("providerPublishTime", 0),
            "url": item.get("link", "")
        }
        for item in raw_news
    ]

__all__ = ["router", "get_news_sentiment"]
