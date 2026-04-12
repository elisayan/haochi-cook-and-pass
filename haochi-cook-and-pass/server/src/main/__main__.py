import asyncio
import websockets

client_connections = set()

async def register_client(websocket):
    client_connections.add(websocket)
    try:
        async for message in websocket:
            print(f"Ricevuto: {message}")
        for client in client_connections: # Broadcast to all clients
                await client.send(f"Echo: {message}")
    finally:
        client_connections.remove(websocket)

async def main():
    async with websockets.serve(register_client, "localhost", 8765):
        print("Server WebSocket in ascolto su ws://localhost:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())