import websockets
import asyncio

PORT = 8855

print(f"Server listening to port {PORT}")

connected = set()


async def echo(ws, path):
    print("A client just connected")
    connected.add(ws)
    try:
        async for message in ws:
            print(f"Received message from client: {message} - {path}")
            for conn in connected:
                if conn != ws:
                    await conn.send(f"I got from someone: {message}")
    except websockets.exceptions.ConnectionClosed as e:
        print("Aclient just disconnected")


start_server = websockets.serve(echo, "localhost", PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
