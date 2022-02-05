# Websockets Project

## Basic example from YouTube video

[How to Create a WebSocket Server/Client in Python](https://www.youtube.com/watch?v=SfQd1FdcTlI)

## Official tutorial

[Introduction to websockets](https://websockets.readthedocs.io/en/stable/intro/tutorial1.html)

### Http test server

We can test our js and html code by running an HTTP test server
```commandline
python -m websockets ws://localhost:8001/
```

### Websockets interactive client

You cannot test the WebSocket server with a web browser like you tested the HTTP server. 
However, you can test it with websockets’ interactive client.

```
$ python -m websockets ws://localhost:8001/
```

### Server handler while loop
The **while await websocket.recv() / try catch** pattern is so common that websockets 
provides a shortcut for iterating over messages received on the connection until 
the client disconnects:
```
async def handler(websocket):
    async for message in websocket:
        print(message)
```

## Part 2

### Added second player
We want to play from two different web browsers: 2 players 

### Added a game watcher
We want to be able to invite people to watch the game.
To achieve this goal we are adding a watch key and use the more efficient **broadcasting pattern**


