import { createBoard, playMove } from "./connect4.js";

window.addEventListener("DOMContentLoaded", () => {
  // Initialize the UI.
  const board = document.querySelector(".board");
  createBoard(board);

  // Open the WebSocket connection and register event handlers.
  const websocket = new WebSocket(getWebSocketServer());
  // capture event onOpen websocket and send init message to server
  initGame(websocket)
  sendMoves(board, websocket);
  // response from websockets server
  receiveMoves(board, websocket);
});

// fleshing out the body of the main js code

function getWebSocketServer() {
  if (window.location.host === "pajmd.github.io") {
    return "wss://ptech-wbs.herokuapp.com/";
  } else if (window.location.host === "localhost:8000") {
    return "ws://localhost:8001/";
  } else {
    throw new Error(`Unsupported host: ${window.location.host}`);
  }
}


// Sending a move to the server
function sendMoves(board, websocket) {
  // When clicking a column, send a "play" event for a move in that column.
  board.addEventListener("click", ({ target }) => {
    const column = target.dataset.column;
    // Ignore clicks outside a column.
    if (column === undefined) {
      return;
    }
    const event = {
      type: "play",
      column: parseInt(column, 10),
    };
    websocket.send(JSON.stringify(event));
  });
}

function showMessage(message) {
  window.setTimeout(() => window.alert(message), 50);
}

function receiveMoves(board, websocket) {
  websocket.addEventListener("message", ({ data }) => {
    const event = JSON.parse(data);
    switch (event.type) {
      case "init":
        document.querySelector(".join").href = "?join=" + event.join;
        document.querySelector(".watch").href = "?watch=" + event.watch;
        break;
      case "play":
        // Update the UI with the move.
        playMove(board, event.player, event.column, event.row);
        break;
      case "win":
        showMessage(`Player ${event.player} wins!`);
        // No further messages are expected; close the WebSocket connection.
        websocket.close(1000);
        break;
      case "error":
        showMessage(event.message);
        break;
      default:
        throw new Error(`Unsupported event type: ${event.type}.`);
    }
  });
}

function initGame(websocket) {
  websocket.addEventListener("open", () => {
    // Send an "init" event for the first player.
    let event = { type: "init" };
    // Parsing the page URL
    const page_query_string = window.location.search
    // Returns an object key-value
    const params = new URLSearchParams(page_query_string);
    if (params.has("join")) {
      // Second player joins an existing game.
      event.join = params.get("join");
    }
    else if (params.has("watch")) {
      event.watch = params.get("watch");
    }
    else {
      // First player starts a new game.
    }
    websocket.send(JSON.stringify(event));
  });
}


