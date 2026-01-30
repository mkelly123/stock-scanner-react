# # from alpaca.data.historical import StockHistoricalDataClient
# # from alpaca.data.requests import StockBarsRequest
# # from alpaca.data.timeframe import TimeFrame
# import pandas as pd
# from dotenv import load_dotenv 
# import os

# # Load .env file 
# load_dotenv()

# # Read keys from environment variables
# ALPACA_API_KEY = os.getenv("ALPACA_API_KEY") 
# ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

# # Initialize Alpaca client with secure keys 
# client = StockHistoricalDataClient(ALPACA_API_KEY, ALPACA_SECRET_KEY)

# def fetch_intraday_alpaca(symbol: str) -> pd.DataFrame:
#     """
#     Fetch 1‑minute intraday bars from Alpaca (real‑time, free).
#     """
#     try:
#         request = StockBarsRequest(
#             symbol_or_symbols=symbol,
#             timeframe=TimeFrame.Minute,
#             limit=500
#         )
#         bars = client.get_stock_bars(request)
#         df = bars.df

#         if df.empty:
#             print(f"[WARN] Alpaca returned empty data for {symbol}")
#         return df

#     except Exception as e:
#         print(f"[ERROR] Alpaca fetch failed for {symbol}: {e}")
#         return pd.DataFrame()
