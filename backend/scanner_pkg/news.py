from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from data_providers.finnhub_provider import get_company_news

router = APIRouter()

class NewsItem(BaseModel):
    symbol: str
    headline: str
    source: str
    summary: str
    timestamp: int
    url: str

@router.get("/news/{symbol}", response_model=List[NewsItem])
def news(symbol: str):
    print(">>> NEWS ENDPOINT CALLED:", symbol)
    return get_company_news(symbol)
