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
        #La posizione viene scelta dall'utente che ha avviato la partita
        self.score = 0.0 #punteggio del giocatore all'interno della partitaoikgt
        self.ingr_id = None #identificativo dell'utente all'interno della partita come nome di un ingrediente

    def disconnect(self):
        self.state = PlayerState.DISCONNECTED
    
    def reconnect(self, websocket):
        self.websocket = websocket
        self.state = PlayerState.CONNECTED

