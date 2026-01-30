from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.websocket_routes import router as ws_router
from backend.scanner import router as scanner_router
from backend.news import router as news_router
from fastapi import WebSocket

from fastapi.responses import PlainTextResponse
from fastapi.exceptions import RequestValidationError
from starlette.websockets import WebSocketDisconnect



import os
print(">>> RUNNING BACKEND FROM:", os.getcwd())


app = FastAPI()
print(">>> ROUTERS MOUNTED:", app.routes)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.middleware("http")
# async def log_every_request(request, call_next):
#     # Skip logging for WebSocket upgrade requests
#     if request.url.path.startswith("/ws/"):
#         return await call_next(request)

#     print(">>> INCOMING REQUEST:", request.url.path)
#     return await call_next(request)

@app.middleware("http") 
async def log_every_request(request: Request, call_next): 
    if request.scope["type"] == "websocket": 
        return await call_next(request) 
    print(">>> INCOMING REQUEST:", request.url.path) 
    return await call_next(request)

@app.exception_handler(WebSocketDisconnect)
async def websocket_disconnect_handler(request, exc):
    print(">>> WS DISCONNECTED:", exc)
    return PlainTextResponse("WebSocket disconnected", status_code=400)


print(">>> INCLUDING WS ROUTER")
app.include_router(ws_router)

print(">>> INCLUDING SCANNER ROUTER")
app.include_router(scanner_router, prefix="/api")

print(">>> INCLUDING NEWS ROUTER")
app.include_router(news_router)

print(">>> FINAL ROUTES:", [route.path for route in app.routes])
