import cv2
import asyncio
import websockets
import struct

video_path = "/workspace/test/test_gouget_cut.mp4"
FPS = 1

async def sender():
    cap = cv2.VideoCapture(video_path)
    async with websockets.connect("ws://0.0.0.0:8765") as ws:
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
