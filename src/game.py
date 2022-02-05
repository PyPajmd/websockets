import asyncio
import websockets
import json
from connect4 import PLAYER1, PLAYER2, Connect4
import secrets
import os
import signal


# Global dictionary to keep track of the games and partners
JOIN = {}
WATCH = {}
PORT = int(os.environ.get("PORT", "8001"))


async def error(websocket, message):
    event = {
        "type": "error",
        "message": message,
    }
    await websocket.send(json.dumps(event))


async def start(websocket, path):
    game = Connect4()
    connected = {websocket}

    join_key = secrets.token_urlsafe(12)
    watch_key = secrets.token_urlsafe(12)
    partnered_up = []
    JOIN[join_key] = game, connected, partnered_up
    WATCH[watch_key] = game, connected

    # send back to the first connected player the url to communicate to the second player over the phone
    try:
        event = {
            "type": "init",
            "join": join_key,
            "watch": watch_key
        }
        await websocket.send(json.dumps(event))
        print(f"From {path} first player started game id: {id(game)}, url: {join_key}")
        # while True:
        #     message = await websocket.recv()
        #     print(f"First player sent: {message}")
        await play(websocket, game, PLAYER1, connected, partnered_up)
    except Exception as e:
        print(f"Something happened: {e}")
    finally:
        print("clearing the game")
        print(f"PLAYER1 removing its socket")
        connected.remove(websocket)
        if join_key in JOIN:
            print(f"PLAYER1 removing join key: {join_key}")
            del JOIN[join_key]
        else:
            print(f"PLAYER1 join key {join_key} already removed")


async def watch(websocket, watch_key):
    # Find the Connect Four game.
    try:
        game, connected = WATCH[watch_key]
    except KeyError:
        await error(websocket, "Game not found.")
        return
    # Register to receive moves from this game.
    connected.add(websocket)
    try:
        for player, column, row in game.get_moves():
            event = {
                "type": "play",
                "player": player,
                "row": row,
                "column": column
            }
            await websocket.send(json.dumps(event))
        await websocket.wait_closed()
    finally:
        print("Watcher removes its connection")
        connected.remove(websocket)
        if not connected:
            print(f"Connection set is empty, removing watch key {watch_key}")
            # We would need to keep track of the watchers to remove the key
            # or indeed let the start remove watch of join keys.
            del WATCH[watch_key]


async def join(websocket, join_key):
    # Find the Connect Four game.
    try:
        game, connected, partnered_up = JOIN[join_key]
    except KeyError:
        await error(websocket, "Game not found.")
        return

    # Register to receive moves from this game.
    connected.add(websocket)
    partnered_up.append(PLAYER2)
    try:

        # Temporary - for testing.
        print("second player joined game", id(game))
        # async for message in websocket:
        #     print("second player sent", message)
        await play(websocket, game, PLAYER2, connected, partnered_up)

    finally:
        print(f"PLAYER2 removing its socket")
        connected.remove(websocket)
        if join_key in JOIN:
            print(f"PLAYER2 removing join key: {join_key}")
            del JOIN[join_key]
        else:
            print(f"PLAYER2 join key {join_key} already removed")


async def play(websocket, game, player, connected, partnered_up):
    async for json_message in websocket:
        message = json.loads(json_message)
        if message["type"] == "play":
            if partnered_up:
                try:
                    row = game.play(player, column=message["column"])
                    event = {
                        "type": "play",
                        "player": player,
                        "row": row,
                        "column": message["column"]
                    }
                    # for w in connected:
                    #     await w.send(json.dumps(event))
                    #     if game.winner:
                    #         event = {
                    #             "type": "win",
                    #             "player": player,
                    #         }
                    #         await w.send(json.dumps(event))

                    # Using a more efficient broadcast
                    websockets.broadcast(connected, json.dumps(event))
                    if game.winner:
                        event = {
                            "type": "win",
                            "player": player,
                        }
                        websockets.broadcast(connected, json.dumps(event))
                except RuntimeError as e:
                    event = {
                        "type": "error",
                        "message": str(e)
                    }
                    await websocket.send(json.dumps(event))
            else:
                event = {
                    "type": "error",
                    "message": "Wait for a partner to play"
                }
                await websocket.send(json.dumps(event))


async def handler(websocket, path):
    print("A new player just joined")
    message = await websocket.recv()
    event = json.loads(message)
    assert event["type"] == "init"
    if "join" in event:
        # second player joining the party
        await join(websocket, event["join"])
    elif "watch" in event:
        await watch(websocket, event["watch"])
    else:
        await start(websocket, path)


async def main():
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
    async with websockets.serve(handler, "", PORT):
        await stop


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        print(f"__main__ is over: {e}")
