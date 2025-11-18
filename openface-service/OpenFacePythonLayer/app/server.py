# Ce module va recevoir les frame par websocket et les écrit dans /dev/video0 avec ffmpeg.

import asyncio
import websockets
import numpy as np
import cv2
import subprocess
import json
import pandas as pd

WIDTH = 640
HEIGHT = 480

ffmpeg = subprocess.Popen([
    "ffmpeg", "-y",
    "-f", "rawvideo", "-pix_fmt", "bgr24",
    "-s", f"{WIDTH}x{HEIGHT}", "-r", "30",
    "-i", "-", "-f", "v4l2", "/dev/video0"
], stdin=subprocess.PIPE)

async def write_frame(websocket):
    async for message in websocket:
        frame = np.frombuffer(message, dtype=np.uint8)
        if frame.size == WIDTH * HEIGHT * 3:
            frame = frame.reshape((HEIGHT, WIDTH, 3))
            ffmpeg.stdin.write(frame.tobytes())

async def gaze_sender() :
    # uri_decision = "ws://172.26.128.105:8082"
    # async with websockets.connect(uri=uri_decision) as ws:
    while True:
        df = pd.read_csv("/workspace/data/data.csv")
        last_row = df.tail(1)
        print(last_row)
        print(type(last_row))
        # data_string = json.dump()
        # await ws.send(data_string)
        await asyncio.sleep(1)  # target FPS
    


async def main() :
    asyncio.create_task(gaze_sender())
    
    port_websocket = 8081
    async with websockets.serve(write_frame, "0.0.0.0", port_websocket):
        print(f"WebSocket server running on ws://0.0.0.0:{port_websocket}")
        await asyncio.Future() 

if __name__ == "__main__" :
    asyncio.run(main())