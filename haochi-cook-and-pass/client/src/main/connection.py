import asyncio
import websockets
import json
from queue import Queue

msg_queue = Queue()   # Messaggi in entrata (dal Server al Client)
send_queue = Queue()  # Messaggi in uscita (dal Client al Server)
running = True
network_status = {
    "server_disconnected": False
} #dizionario condiviso che avverte il giocatore quando il server si sconnete

async def websocket_client():
    global running
    uri = "ws://localhost:8765"

    websocket = None
    while running: 
        try:
            print("Tentativo di connessione al server")
            websocket = await websockets.connect(uri)
            print("Connesso al server!")
            #Il server si è connesso correttamente o riconnesso
            network_status["server_disconnected"] = False

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
                except websockets.exceptions.ConnectionClosed as e:
                    print(f"Connessione chiusa. Codice: {e.rcvd.code}, Motivo: {e.rcvd.reason}")
                    network_status["server_disconnected"] = True   
                    # Lanciata eccezione così che entrambi i task si blocchino
                    raise
            # Esegue entrambi i task contemporaneamente in background. Se il server crasha allora la connessione si rompe e websocket.recv() lancia immediatamente ConnectionClosed.
            # Nel frattempo però se send_handler non ha da inviare alcun messaggio al server allora non si accorge che la connessione è caduta
            # Senza che recv_handler lanci eccezione (raise)  syncio.gather resterebbe appeso ad aspettare send_handler e il codice non eseguirà mai finally
            await asyncio.gather(send_handler(), recv_handler())

        except Exception as e:
            print(f"Errore di rete (server spento o non raggiungibile): {e}")
            network_status["server_disconnected"] = True #server non raggiungibile o errore di rete

        finally:
            if websocket:
                await websocket.close()
            print("websocket chiuso")
        if running:
            print("Tentativo di riconnessione tra 3 secondi")
            await asyncio.sleep(3)    

def start_network():
    """Funzione punto di ingresso per il Thread."""
    asyncio.run(websocket_client())

def shutdown():
    global running
    print("chiusura rete...")
    running = False