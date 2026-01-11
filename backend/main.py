from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scanner import scan_universe

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/scan")
def scan(mode: str, universe: str):
    tickers = [t.strip().upper() for t in universe.split(",")]
    results = scan_universe(tickers, mode=mode)
    return results
