import pygame
import threading
import json

from .connection import start_network, msg_queue, send_queue
from .templates import menu_view, lobby_view

def start_game():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    
    state = "MENU"  # Altri stati "LOBBY", "IN_GAME", ecc.
    game_code = "" 
    
    button_rect = pygame.Rect(350, 250, 100, 50)
    font = pygame.font.SysFont("Arial", 24)
    code_font = pygame.font.SysFont("Arial", 48, bold=True)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if state == "MENU" and event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    payload = json.dumps({"action": "START_GAME", "user": "Player1"})
                    send_queue.put(payload)

        # Logica per processare i messaggi in arrivo dal Server
        while not msg_queue.empty():
            raw_msg = msg_queue.get()
            try:
                data = json.loads(raw_msg)
                if data.get("action") == "ROOM_CREATED":
                    game_code = data.get("code") # Aggiorna il Model locale
                    state = "LOBBY"
                    #todo: altre azioni da processare
            except:
                print(f"Messaggio non strutturato: {raw_msg}")

        # Rendering: chiamata alle funzioni di disegno in base allo stato attuale
        if state == "MENU":
            menu_view.draw(screen, button_rect, font)
        elif state == "LOBBY":
            lobby_view.draw(screen, game_code, font, code_font)
        #todo: altri stati e relative view
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    threading.Thread(target=start_network, daemon=True).start()
    start_game()
