import uuid

class RoomState:
    INIT = "INIT"
    READY = "READY"
    IN_GAME = "IN_GAME"
    OVER = "OVER"


class Room:
    def __init__(self, room_code):
        self.code = room_code
        self.state = RoomState.INIT
        self.players = {}
        self.host_id = None

    def add_player(self, player):
        if len(self.players) >= 8:
            #raise Exception("Room full")
            return False
        
        self.players[player.id] = player
        player.room_code = self.code

        if self.host_id is None:
            self.host_id = player.id

        self._update_state()
        return True

    def remove_player(self, player_id):
        if player_id in self.players:
            del self.players[player_id]
            
        # se era host, assegna nuovo host (il primo rimasto) o None se vuota
        if player_id == self.host_id and self.players:
            self.host_id = next(iter(self.players.keys()))
        elif not self.players:
            self.host_id = None
        
        self._update_state()

    def _update_state(self): #aggiorna lo stato della stanza in base ai giocatori
        if self.state in [RoomState.IN_GAME, RoomState.OVER]:
            return  # non cambiare stato durante la partita
        
        player_count = len(self.players)
        
        if player_count < 2:
            self.state = RoomState.INIT
        elif 2 <= player_count <= 8:
            self.state = RoomState.READY
