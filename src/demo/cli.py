import websockets
import asyncio


async def listen():
    url = "ws://localhost:8855"

    async with websockets.connect(url) as ws:
        print("Client connected")
        await ws.send("Here I am")
        while True:
            msg = await ws.recv()
            print(msg)

asyncio.get_event_loop().run_until_complete(listen())

