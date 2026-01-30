from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from backend.scanner_pkg.scan_universe import scan_universe

print(">>> LOADED WS ROUTE X1 <<<")



router = APIRouter()

@router.websocket("/ws/scan")
async def websocket_scan(websocket: WebSocket):
    print(">>> WS HANDLER ENTERED") 
    await websocket.accept() 
    await websocket.send_json({ "type": "handshake", "message": "hello from backend" })
    print(">>> ROUTER OBJECT:", router)

    try:
        while True:
            results = scan_universe(
                universe=["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"],
                filter_type="momentum"
            )

            for row in results:
                print("Sending row:", row)
                await websocket.send_json({
                    "type": "scanner_update",
                    "data": row
                })

            await asyncio.sleep(1)

    except WebSocketDisconnect:
        print("[INFO] WebSocket client disconnected")
print(">>> ROUTER FINAL:", router)
