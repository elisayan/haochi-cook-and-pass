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
        self.position = None #posizione all'interno del giro della partita
        self.score = 0.0 #punteggio del giocatore all'interno della partitaoikgt

    def disconnect(self):
        self.state = PlayerState.DISCONNECTED
    
    def reconnect(self, websocket):
        self.websocket = websocket
        self.state = PlayerState.CONNECTED

