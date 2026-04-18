import asyncio
import pygame
import websockets
import threading
import json
from queue import Queue

msg_queue = Queue()
send_queue = Queue()

async def websocket_client():
    uri = "ws://localhost:8765"
    try:
        async with websockets.connect(uri) as websocket:
            print("Connesso al server!")

            async def send_handler():
                while True:
                    if not send_queue.empty():
                        msg = send_queue.get()
                        await websocket.send(msg)
                    # Importantissimo: un piccolo sleep per non saturare la CPU
                    await asyncio.sleep(0.1) 

            async def recv_handler():
                try:
                    async for message in websocket:
                        msg_queue.put(message)
                except websockets.exceptions.ConnectionClosed:
                    print("Connessione chiusa dal server")

            # Avviamo entrambi e aspettiamo che finiscano (non dovrebbero mai finire)
            await asyncio.gather(send_handler(), recv_handler())
            
    except Exception as e:
        print(f"Errore di connessione: {e}")

def start_network():
    asyncio.run(websocket_client())

def start_game():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    
    # Stato del gioco locale (il nostro "Model" nel client)
    game_code = "" 
    
    button_rect = pygame.Rect(350, 250, 100, 50)
    font = pygame.font.SysFont("Arial", 24)
    code_font = pygame.font.SysFont("Arial", 48, bold=True)

    running = True
    while running:
        screen.fill((255, 255, 255))

        # Disegno bottone (View)
        pygame.draw.rect(screen, (0, 200, 0), button_rect)
        btn_text = font.render("START", True, (255, 255, 255))
        screen.blit(btn_text, (button_rect.x + 15, button_rect.y + 10))

        # Disegno del codice se presente (View)
        if game_code:
            label = font.render("Codice Stanza:", True, (0, 0, 0))
            code_text = code_font.render(game_code, True, (0, 0, 255))
            screen.blit(label, (340, 150))
            screen.blit(code_text, (355, 180))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    payload = json.dumps({"action": "START_GAME", "user": "Player1"})
                    send_queue.put(payload)

        # Processo messaggi dal server (Controller)
        while not msg_queue.empty():
            raw_msg = msg_queue.get()
            try:
                data = json.loads(raw_msg)
                if data.get("action") == "ROOM_CREATED":
                    game_code = data.get("code") # Aggiorna il Model locale
            except:
                print(f"Messaggio non strutturato: {raw_msg}")

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    threading.Thread(target=start_network, daemon=True).start()
    start_game()
