# from dotenv import load_dotenv
# import os
# from alpaca.data.historical import StockHistoricalDataClient
# from alpaca.data.requests import StockBarsRequest
# from alpaca.data.timeframe import TimeFrame

# load_dotenv()

# print("Loaded .env file")

# api_key = os.getenv("ALPACA_API_KEY")
# secret_key = os.getenv("ALPACA_SECRET_KEY")

# print("API KEY:", api_key)
# print("SECRET KEY:", secret_key)

# client = StockHistoricalDataClient(api_key, secret_key)

# request = StockBarsRequest(
#     symbol_or_symbols="AAPL",
#     timeframe=TimeFrame.Minute,
#     limit=5
# )

# bars = client.get_stock_bars(request)
# print(bars.df.head())
