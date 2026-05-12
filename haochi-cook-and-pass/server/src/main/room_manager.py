import random
import string
from .room import Room

class RoomManager:
    def __init__(self):
        self.rooms = {}

    def generate_code(self, length=4):
        return ''.join(random.choices(string.ascii_uppercase, k=length))

    def create_room(self):
        code = self.generate_code()
        while code in self.rooms:
            code = self.generate_code()
        
        new_room = Room(code)
        self.rooms[code] = new_room
        return new_room

    def get_room(self, code):
        return self.rooms.get(code)

    def remove_room(self, code):
        """Elimina la stanza e resetta tutti i player coinvolti."""
        if code in self.rooms:
            room = self.rooms[code]
            for player in room.players.values():
                player.room_code = None
                player.position = None
            room.players.clear()
            del self.rooms[code]
            print(f"Manager: Room {code} eliminata e player resettati.")

    def remove_player(self, player_id):
        """Cerca un player in tutte le stanze e lo rimuove (utile per disconnessioni improvvise)."""
        for code, room in list(self.rooms.items()):
            if player_id in room.players:
                is_host = (player_id == room.host_id)
                room.remove_player(player_id)
                
                # Se la stanza è vuota O se l'host se n'è andato, chiudiamo tutto
                if len(room.players) == 0 or is_host:
                    self.remove_room(code)
                return True
        return False