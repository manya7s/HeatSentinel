import asyncio
import websockets
import json

clients = set()

async def ws_handler(websocket, path):
    clients.add(websocket)
    try:
        async for _ in websocket:  # handle incoming messages if any
            pass
    finally:
        clients.remove(websocket)

async def start_server():
    async with websockets.serve(ws_handler, "0.0.0.0", 8765):
        print("WebSocket server running on ws://0.0.0.0:8765")
        await asyncio.Future()  # run forever

async def send_update(message: dict):
    if clients:
        data = json.dumps(message)
        await asyncio.gather(*[ws.send(data) for ws in clients])

if __name__ == "__main__":
    asyncio.run(start_server())
