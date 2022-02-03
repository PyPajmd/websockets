import asyncio
import websockets
import json
from connect4 import PLAYER1, PLAYER2, Connect4


async def handler1(websocket):
    try:
        print(f"From {websocket.id} @ {websocket.remote_address} is connected")
        while True:
            try:
                message = await websocket.recv()
                print(f"From {websocket.id} @ {websocket.remote_address}: {message}")
                if message == "end":
                    # server closes the connection requested by the client
                    await websocket.close()
                    print("This code is upon receiving end message from client")
            except websockets.exceptions.ConnectionClosedOK:
                print(f"Client forced close ('end' or kill -3). Client ID: {websocket.id}")
                break
    finally:
        print(f"This handler is done with {websocket.id}")


# while loop and the try of handler_1 can be replaced with a common websockets pattern
# async for - in websocket
async def handler_2(websocket):
    async for message in websocket:
        print(message)

# Checking the server can send messages to the js and js processes them
async def handler_3(websocket):
    for player, column, row in [
        (PLAYER1, 3, 0),
        (PLAYER2, 3, 1),
        (PLAYER1, 4, 0),
        (PLAYER2, 4, 1),
        (PLAYER1, 2, 0),
        (PLAYER2, 1, 0),
        (PLAYER1, 5, 0),
    ]:
        event = {
            "type": "play",
            "player": player,
            "column": column,
            "row": row,
        }
        await websocket.send(json.dumps(event))
        await asyncio.sleep(0.5)
    event = {
        "type": "win",
        "player": PLAYER1,
    }
    await websocket.send(json.dumps(event))


async def handler(websocket):
    game = Connect4()
    player = PLAYER1
    async for json_message in websocket:
        message = json.loads(json_message)
        print(message)
        print(f"Playing {player}")
        if message["type"] == "play":
            try:
                column = message["column"]
                row = game.play(player, column)
                if game.last_player_won:
                    event = {
                        "type": "win",
                        "player": player,
                    }
                else:
                    event = {
                        "type": "play",
                        "player": player,
                        "row": row,
                        "column": column
                    }
                await websocket.send(json.dumps(event))
            except RuntimeError as e:
                event = {
                    "type": "error",
                    "message": str(e)
                }
                await websocket.send(json.dumps(event))
            finally:
                player = PLAYER2 if game.last_player == PLAYER1 else PLAYER1
                print(f"next player {player}")



async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        print(f"__main__ is over: {e}")
