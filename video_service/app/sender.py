import cv2
import asyncio
import websockets
import struct


video_path = "/workspace/data/test_gouget_cut.mp4"
uri = "ws://192.168.178.46:8080"
# uri = "ws://0.0.0.0:8080"
FPS = 30

async def sender():
    cap = cv2.VideoCapture(video_path)
    async with websockets.connect(uri=uri) as ws:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            # Downscale if needed
            frame = cv2.resize(frame, (640, 480))
            await ws.send(frame.tobytes())
            await asyncio.sleep(1/FPS)  # target FPS
    cap.release()

asyncio.run(sender())
