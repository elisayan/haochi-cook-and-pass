import asyncio
import websockets
import json
from queue import Queue

msg_queue = Queue()   # Messaggi in entrata (dal Server al Client)
send_queue = Queue()  # Messaggi in uscita (dal Client al Server)
running = True

async def websocket_client():
    global running
    uri = "ws://localhost:8765"

    websocket = None

    try:
        websocket = await websockets.connect(uri)
        print("Connesso al server!")

        async def send_handler():
            while running:
                if not send_queue.empty():
                    msg = send_queue.get()
                    await websocket.send(msg)
                await asyncio.sleep(0.1)

        async def recv_handler():
            try:
                while running:
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=0.2)
                        msg_queue.put(message)
                    except asyncio.TimeoutError:
                        continue
            except websockets.exceptions.ConnectionClosed:
                print("Connessione chiusa")

        await asyncio.gather(send_handler(), recv_handler())

    except Exception as e:
        print(f"Errore di rete: {e}")

    finally:
        if websocket:
            await websocket.close()
        print("websocket chiuso")

def start_network():
    """Funzione punto di ingresso per il Thread."""
    asyncio.run(websocket_client())

def shutdown():
    global running
    print("chiusura rete...")
    running = False