import asyncio
import json
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import zmq
import zmq.asyncio

# -------------------------------
# WebSocket manager
# -------------------------------
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        disconnected = []
        for conn in self.active_connections:
            try:
                await conn.send_text(message)
            except WebSocketDisconnect:
                disconnected.append(conn)
        for conn in disconnected:
            self.disconnect(conn)

manager = ConnectionManager()

# -------------------------------
# Dummy ZMQ subscriber (background task)
# -------------------------------
async def zmq_subscriber():
    print("zmq_subscriber started")
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://172.26.128.105:8081")
    socket.setsockopt(zmq.SUBSCRIBE, b"")
    print("Listening on : tcp://172.26.128.105:8081...")
    try:
        while True:
            data = await socket.recv_json()
            x = data["gaze_angle_x"]
            y = data["gaze_angle_y"]
            await manager.broadcast(json.dumps({"x": x, "y": y}))
            await asyncio.sleep(0.03)

    except asyncio.CancelledError:
        print("zmq_subscriber cancelled")
        raise  # important to propagate cancellation

# -------------------------------
# Lifespan for background task
# -------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(zmq_subscriber())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("zmq_subscriber stopped")

# -------------------------------
# FastAPI app
# -------------------------------
app = FastAPI(lifespan=lifespan)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def get_index():
    with open("static/index.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/interface")
async def get_interface() :
    with open("static/interface.html") as f :
        return HTMLResponse(content=f.read())
    
    
# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await asyncio.sleep(0.03)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("WebSocket disconnected")
