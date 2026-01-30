from polygon import RESTClient
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("POLYGON_API_KEY")

client = RESTClient(api_key)

# Fetch 5 recent 1-minute bars for AAPL
bars = client.get_aggs("AAPL", 1, "minute", limit=5)
for bar in bars:
    print(bar)
