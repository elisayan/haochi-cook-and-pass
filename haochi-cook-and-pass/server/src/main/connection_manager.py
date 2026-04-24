import asyncio
from .player import Player

class ConnectionManager:
    def __init__(self):
        self.connected_players = {}

    def add_player(self, websocket, player_id):
        player = Player(player_id=player_id, websocket=websocket)
        self.connected_players[websocket] = player
        return player

    def remove_player(self, websocket):
        return self.connected_players.pop(websocket, None)

    async def broadcast(self, message, exclude=None):
        targets = [ws for ws in self.connected_players if ws != exclude]
        if targets:
            await asyncio.gather(*[ws.send(message) for ws in targets], return_exceptions=True)

# Istanza globale da usare negli altri file
manager = ConnectionManager()