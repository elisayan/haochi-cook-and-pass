import uuid

class RoomState:
    INIT = "INIT"
    READY = "READY"
    IN_GAME = "IN_GAME"
    OVER = "OVER"


class Room:
    def __init__(self, name):
        self.code = name
        self.players = {}
        self.state = RoomState.INIT

    def add_player(self, player):
        self.players[player.id] = player
        if len(self.players) >= 2:
            self.state = RoomState.READY

    def remove_player(self, player_id):
        if player_id in self.players:
            del self.players[player_id]
            if len(self.players) < 2:
                self.state = RoomState.INIT
    
    #def get_player