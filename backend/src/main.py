from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Trading Bot API",
    description="Core API for the AI-Powered Trading Bot Platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI Trading Bot API is running", "status": "ok"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "services": {"database": "pending", "redis": "pending"}}

# Real-time WebSocket endpoint stub
@app.websocket("/ws/market")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo market data: {data}")
    except WebSocketDisconnect:
        logger.info("Client disconnected")