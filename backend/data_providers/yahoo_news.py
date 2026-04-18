import requests

def get_news(symbol: str):
    """
    Fetch real news for a stock symbol using Yahoo Finance's public search API.
    No API key required.
    """
    url = f"https://query1.finance.yahoo.com/v1/finance/search?q={symbol}"
    resp = requests.get(url, timeout=5)
    data = resp.json()

    news_items = []

    for item in data.get("news", []):
        news_items.append({
            "symbol": symbol,
            "headline": item.get("title", ""),
            "source": item.get("publisher", ""),
            "summary": item.get("summary", ""),
            "url": item.get("link", ""),
            "timestamp": item.get("providerPublishTime", 0)
        })

    return news_items
