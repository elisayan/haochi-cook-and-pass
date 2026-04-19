import asyncio
import websockets
import json
import uuid

from .connection_manager import manager
from .controller_server import ACTION_HANDLERS 

async def register_client(websocket):
    player_id = str(uuid.uuid4())[:8]
    player = manager.add_player(websocket, player_id)
    print(f"Player {player_id} connesso.")

    try:
        # Ciclo di ricezione messaggi
        async for message in websocket:
            try:
                data = json.loads(message)
                action = data.get("action")

                handler = ACTION_HANDLERS.get(action)
                
                if handler:
                    # Eseguiamo le funzioni presenti in ACTION_HANDLERS
                    await handler(websocket, player, data)
                else:
                    print(f"Azione non riconosciuta: {action}")

            except json.JSONDecodeError:
                print(f"Errore: messaggio non JSON ricevuto da {player_id}")

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        manager.remove_player(websocket)
        print(f"Player {player_id} rimosso.")

async def main():
    async with websockets.serve(register_client, "localhost", 8765):
        print("Server WebSocket in ascolto su ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())