# config.py

# Default stock universe
STOCK_UNIVERSE = [
    "AAPL", "MSFT", "NVDA", "AMZN", "META",
    "TSLA", "AMD", "NFLX", "GOOGL", "BABA"
]

# ETF universe
ETF_UNIVERSE = [
    "SPY", "QQQ", "IWM", "VTI"
]

# Delay between API calls (politeness + rate limiting)
SLEEP_SECONDS = 1
