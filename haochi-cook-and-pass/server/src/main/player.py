from enum import Enum
from websockets import WebSocketServerProtocol

class PlayerState(Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"

class Player:
    def __init__(self, player_id, websocket: WebSocketServerProtocol):
        self.id = player_id
        self.websocket = websocket
        self.state = PlayerState.CONNECTED
        self.room_code = None

    def disconnect(self):
        self.state = PlayerState.DISCONNECTED
    
    def reconnect(self, websocket):
        self.websocket = websocket
        self.state = PlayerState.CONNECTED

