import random
import string
import asyncio

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

        self.rooms[code] = Room(code)

        print(f"Room creata: {code}")
        return code

    def get_room(self, code):
        return self.rooms.get(code)

    def remove_player(self, player_id):
        for code, room in self.rooms.items():
            if player_id in room.players:
                room.remove_player(player_id)

                print(f"Player {player_id} rimosso da {code}")

                # se la room è vuota -> cancella
                if len(room.players) == 0:
                    del self.rooms[code]
                    print(f"Room {code} eliminata")

                return
