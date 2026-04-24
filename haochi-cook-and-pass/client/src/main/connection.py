import asyncio
import websockets
import json
from queue import Queue

msg_queue = Queue()   # Messaggi in entrata (dal Server al Client)
send_queue = Queue()  # Messaggi in uscita (dal Client al Server)

async def websocket_client():
    uri = "ws://localhost:8765"
    try:
        async with websockets.connect(uri) as websocket:
            print("Connesso al server!")

            # Gestore per l'INVIO dei messaggi
            async def send_handler():
                while True:
                    if not send_queue.empty():
                        msg = send_queue.get()
                        await websocket.send(msg)
                    # Evita di consumare troppa CPU
                    await asyncio.sleep(0.1) 

            # Gestore per la RICEZIONE dei messaggi
            async def recv_handler():
                try:
                    async for message in websocket:
                        msg_queue.put(message)
                except websockets.exceptions.ConnectionClosed:
                    print("Connessione chiusa dal server")

            # Esegue entrambi i compiti contemporaneamente
            await asyncio.gather(send_handler(), recv_handler())
            
    except Exception as e:
        print(f"Errore di rete: {e}")

def start_network():
    """Funzione punto di ingresso per il Thread."""
    asyncio.run(websocket_client())