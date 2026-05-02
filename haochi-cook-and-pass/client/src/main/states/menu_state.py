# menu_state.py
import sys
import pygame
import json
from .base_state import BaseState

class MenuState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.sub_menu = "MAIN"
        self.font = pygame.font.SysFont("Arial", 24)

        self.rects = {
            "start": pygame.Rect(400, 300, 220, 80),
            "tutorial": pygame.Rect(400, 380, 220, 80),
            "exit": pygame.Rect(400, 460, 220, 80),

            "create": pygame.Rect(250, 250, 150, 50),
            "join": pygame.Rect(450, 250, 150, 50)
        }

    def handle_input(self, event, send_queue, model):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.rects:
                return

            if self.sub_menu == "MAIN":
                if self.rects["start"].collidepoint(event.pos):
                    print("Start premuto")
                    self.sub_menu = "ROOM_CHOICE"
                elif self.rects["tutorial"].collidepoint(event.pos):
                    print("TUTORIAL")
                elif self.rects["exit"].collidepoint(event.pos):
                    print("CHIUSURA IN CORSO...")
                    # USA pygame.event.post invece di chiamare direttamente quit
                    # Ma assicurati di uscire subito dal metodo
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                    return  # Importante: esci subito
                    
            elif self.sub_menu == "ROOM_CHOICE":
                if self.rects.get("create") and self.rects["create"].collidepoint(event.pos):
                    send_queue.put(json.dumps({"action": "START_GAME"}))
                elif self.rects.get("join") and self.rects["join"].collidepoint(event.pos):
                    model.switch_to("JOIN_INPUT")