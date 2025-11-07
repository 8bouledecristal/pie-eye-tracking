import asyncio
import websockets
import subprocess
import numpy as np

WIDTH, HEIGHT = 640, 480
# ffmpeg = subprocess.Popen([
#     "ffmpeg", "-y",
#     "-f", "rawvideo", "-pix_fmt", "bgr24",
#     "-s", f"{WIDTH}x{HEIGHT}", "-r", "30",
#     "-i", "-", "-f", "v4l2", "/dev/video2"
# ], stdin=subprocess.PIPE)

async def handler(ws):
    async for message in ws:
        frame = np.frombuffer(message, dtype=np.uint8)
        if frame.size == WIDTH * HEIGHT * 3:
            # ffmpeg.stdin.write(frame)
            frame = frame.reshape(WIDTH, HEIGHT, 3)
            print(frame[WIDTH//2,HEIGHT//2,0])
            
async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()

asyncio.run(main())
