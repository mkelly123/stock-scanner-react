from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from backend.scanner_pkg.scan_universe import scan_universe
from backend.scanner_pkg.top_gainers import get_top_gainers

print(">>> LOADED WS ROUTE X1 <<<")

router = APIRouter()

@router.websocket("/ws/scan")
async def websocket_scan(websocket: WebSocket):
    await websocket.accept()

    await websocket.send_json({
        "type": "handshake",
        "message": "hello from backend"
    })

    try:
        while True:
            # 1. Fetch top gainers dynamically
            symbols = get_top_gainers(limit=20)

            # 2. Run your scanner on those symbols
            results = scan_universe(
                universe=get_top_gainers(limit=20),
                filter_type="momentum"
            )


            # 3. Send results to frontend
            for row in results:
                await websocket.send_json({
                    "type": "scanner_update",
                    "data": row
                })

            await asyncio.sleep(5)

    except WebSocketDisconnect:
        print("[INFO] WebSocket client disconnected")
