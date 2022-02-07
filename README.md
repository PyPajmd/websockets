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

## Part 3
### Deploying to the web
* Port needs to be an environment variable
* We need to catch the SIGTERM signal

### Deploying the websocket server to Heroku
* we create a Procfile to start the web app
* install Heroku cli sudo snap install heroku --classic
* start Heroku
```
heroku login
```
* create Heroku petch-wbs
```
heroku create <app_name>
Creating ⬢ petch-wbs... done
https://petch-wbs.herokuapp.com/ | https://git.heroku.com/petch-wbs.git
```
* pushing code to heroku
```commandline
git push https://git.heroku.com/petch-wbs.git
```
* test websockets server
```commandline
python -m websockets wss://petch-wbs.herokuapp.com/
```
* change main.js to route the open of the websocket according to the path of the HTTP server.
* set up the [GitHub static HTTP server](https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages):
  * Go to the Settings tab of the GitHub repository
  * Select Pages in the menu. 
  * Select the main branch as source and click Save to publish the site or **None** to unpublish it.
  * To the URL suggested must be appended the path of the index.html file.
  
#### (Heroku commands)[https://devcenter.heroku.com/articles/getting-started-with-python#scale-the-app]

```commandline
heroku local&  # for local testing
heroku logs --tail -a petch-wbs
heroku ps -a petch-wbs # show quotas
heroku ps:scale web=0 -a petch-wbs # scales down to 0 the number of dynos running in effect shutting it down
heroku ps:scale web=1 -a petch-wbs # restart the app
```