from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from backend.scanner_pkg.scan_universe import scan_universe
print("Importing scanner.py...")

router = APIRouter()

# ---------------------------------------------------------
# REST API endpoint (unchanged)
# ---------------------------------------------------------
@router.get("/scan/{filter_type}")
async def scan_api(filter_type: str):
    try:
        results = scan_universe(
            universe=["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"],
            filter_type=filter_type
        )
        return results

    except Exception as e:
        print("[ERROR] Scanner crashed:", e)
        return []   # or return {"error": str(e)}

