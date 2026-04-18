import asyncio
import websockets
import json

from .room_manager import RoomManager

client_connections = set()
room_manager = RoomManager()

async def register_client(websocket):
    client_connections.add(websocket)
    print(f"Nuova connessione: {websocket.remote_address}")
    try:
        async for message in websocket:
            print(f"Ricevuto: {message}")
            try:
                data = json.loads(message)
                if data.get("action") == "START_GAME":
                    game_code = room_manager.generate_code(length=4)
                    print(f"Partita avviata! Codice generato: {game_code}")

                    response = json.dumps({"action":"ROOM_CREATED", "code": game_code})

                    # Invia la risposta al client che ha richiesto la partita
                    await websocket.send(response)
            except json.JSONDecodeError:
                pass 

            # BROADCAST SICURO
            if client_connections:
                # Creiamo una copia della lista per evitare errori durante l'iterazione
                # Usiamo asyncio.wait per non bloccare tutto se un client è lento
                message_to_send = f"Update: {message}"
                
                # Invio a tutti, gestendo eventuali errori singolarmente
                disconnected_clients = set()
                for client in client_connections:
                    try:
                        await client.send(message_to_send)
                    except websockets.exceptions.ConnectionClosed:
                        disconnected_clients.add(client)
                
                # Pulizia client morti
                for client in disconnected_clients:
                    client_connections.remove(client)

    except websockets.exceptions.ConnectionClosedError:
        print("Connessione persa con un client.")
    finally:
        if websocket in client_connections:
            client_connections.remove(websocket)
        print("Connessione pulita.")

async def main():
    async with websockets.serve(register_client, "localhost", 8765):
        print("Server WebSocket in ascolto su ws://localhost:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())