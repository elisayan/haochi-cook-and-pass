import asyncio
import websockets
import json
import uuid

from .room_manager import RoomManager
from .player import Player

connected_players = {}
room_manager = RoomManager()

async def register_client(websocket):
    player_id = str(uuid.uuid4())[:8]
    new_player = Player(player_id=player_id, websocket=websocket)
    connected_players[websocket] = new_player
    
    print(f"Player {player_id} collegato.")
    
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                current_player = connected_players.get(websocket)
                if not current_player: continue

                if data.get("action") == "START_GAME":
                    game_code = room_manager.generate_code(length=4)
                    current_player.room_code = game_code
                    
                    response = json.dumps({
                        "action": "ROOM_CREATED", 
                        "code": game_code, 
                        "player_id": current_player.id
                    })
                    await websocket.send(response)
                
                # Esempio di Broadcast selettivo:
                # Invia a tutti gli ALTRI che un giocatore ha fatto qualcosa
                broadcast_msg = json.dumps({"action": "UPDATE", "msg": f"Player {player_id} ha agito"})
                await broadcast(broadcast_msg, exclude=websocket)

            except json.JSONDecodeError:
                print(f"Messaggio non valido: {message}")

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected_players.pop(websocket, None)
        print(f"Player {player_id} disconnesso e rimosso.")

async def broadcast(message, exclude=None):
    if not connected_players:
        return
    targets = [ws for ws in connected_players if ws != exclude]
    if targets:
        await asyncio.gather(*[ws.send(message) for ws in targets], return_exceptions=True)

async def main():
    async with websockets.serve(register_client, "localhost", 8765):
        print("Server WebSocket in ascolto su ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())