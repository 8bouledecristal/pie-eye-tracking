# Ce module va recevoir les frame par websocket et les écrit dans /dev/video0 avec ffmpeg.

import asyncio
import websockets
import numpy as np
import cv2
import subprocess

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


async def main() :
    port_websocket = 8081
    async with websockets.serve(write_frame, "0.0.0.0", port_websocket):
        print(f"WebSocket server running on ws://0.0.0.0:{port_websocket}")
        await asyncio.Future() 

if __name__ == "__main__" :
    asyncio.run(main())