import pygame
import threading
import json

from pygame import event

from .connection import start_network, msg_queue, send_queue
from .templates import menu_view, lobby_view, join_view

def start_game():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    
    state = "MENU"  # Altri stati "LOBBY", "IN_GAME", ecc.
    game_code = "" 
    
    button_rect = pygame.Rect(350, 250, 100, 50)
    font = pygame.font.SysFont("Arial", 24)
    code_font = pygame.font.SysFont("Arial", 48, bold=True)
    main_btn = pygame.Rect(350, 250, 100, 50)
    create_btn = pygame.Rect(250, 250, 150, 50)
    join_btn = pygame.Rect(450, 250, 150, 50)
    sub_menu = "MAIN"
    input_text = ""

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == "MENU":
                    if sub_menu == "MAIN" and main_btn.collidepoint(event.pos):
                        sub_menu = "ROOM_CHOICE"
                    elif sub_menu == "ROOM_CHOICE":
                        if create_btn.collidepoint(event.pos):
                            send_queue.put(json.dumps({"action": "START_GAME"}))
                        elif join_btn.collidepoint(event.pos):
                            state = "JOIN_INPUT" # Passa alla schermata di inserimento

            # GESTIONE TASTIERA (Solo se dobbiamo scrivere il codice)
            if state == "JOIN_INPUT" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Invia il codice al server per tentare di unirsi
                    payload = json.dumps({"action": "JOIN_ROOM", "code": input_text})
                    send_queue.put(payload)
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    # Accetta solo caratteri (limita la lunghezza se necessario)
                    if len(input_text) < 4:
                        input_text += event.unicode.upper()

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
            menu_view.draw(screen, font, sub_menu, main_btn, create_btn, join_btn)
        elif state == "JOIN_INPUT":
            join_view.draw(screen, font, input_text)
        elif state == "LOBBY":
            lobby_view.draw(screen, game_code, font, code_font)
        #todo: altri stati e relative view
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    threading.Thread(target=start_network, daemon=True).start()
    start_game()
