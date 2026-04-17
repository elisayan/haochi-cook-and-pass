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
    pygame.display.set_caption("Haochi Cook and Pass")
    clock = pygame.time.Clock()

    button_rect = pygame.Rect(350, 250, 100, 50)
    button_color = (0, 200, 0)
    font = pygame.font.SysFont("Arial", 24)

    running = True
    while running:
        screen.fill((255, 255, 255))

        pygame.draw.rect(screen, button_color, button_rect)
        text = font.render("START", True, (255, 255, 255))
        screen.blit(text, (button_rect.x + 15, button_rect.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Gestione click bottone
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    print("Bottone cliccato! Invio al server...")
                    # Inviamo un messaggio strutturato (JSON è meglio per il server)
                    payload = json.dumps({"action": "START_GAME", "user": "Player1"})
                    send_queue.put(payload)

        # Process messages from the server
        while not msg_queue.empty():
            msg = msg_queue.get()
            # Handle the message (e.g., update game state)
            print(f"Processing message: {msg}")
        pygame.display.flip()
        clock.tick(60) # Limit to 60 FPS
    pygame.quit()

if __name__ == "__main__":
    threading.Thread(target=start_network, daemon=True).start()
    start_game()
