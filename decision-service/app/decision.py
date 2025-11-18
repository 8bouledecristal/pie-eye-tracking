import asyncio
import websockets
import json


async def get_gaze(websocket):
    async for message in websocket:
        print(message)
        pass


async def main() :
    port_websocket = 8082
    async with websockets.serve(get_gaze, "0.0.0.0", port_websocket):
        print(f"WebSocket server running on ws://0.0.0.0:{port_websocket}")
        await asyncio.Future() 

if __name__ == "__main__" :
    asyncio.run(main())