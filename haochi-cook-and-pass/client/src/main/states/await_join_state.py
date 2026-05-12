import pygame
import json
from .base_state import BaseState

class AwaitJoinState(BaseState):
    def __init__(self, model):
        super().__init__(model)

        self.error_message = ""

        self.rects = {
            "back_arrow": pygame.Rect(20, 20, 60, 50),
            "error_home_btn": pygame.Rect(0, 0, 200, 50)  # Posizione e dimensione da aggiornare dinamicamente
        }

    def handle_input(self, event, send_queue, model):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 1. Se c'è un errore (Popup visibile), gestisci solo il tasto del Popup
            #if model.error_message:
            #    if "error_home_btn" in self.rects:
            if self.rects["error_home_btn"].collidepoint(event.pos):
                        model.error_message = None  # Pulisci l'errore
                        model.switch_to("MENU")     # Torna al menu
                        # Nota: Non serve QUIT_ROOM qui perché la room è già chiusa dal server
            #return
        #todo deve solo aspettare che il host della stanza avvia il gioco
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rects["back_arrow"].collidepoint(event.pos):
                send_queue.put(json.dumps({"action": "QUIT_ROOM"}))
                model.switch_to("MENU")

    def update(self, mouse_pos, screen_width, screen_height):
        pass
    