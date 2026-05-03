#import sys
import pygame
import json
from .base_state import BaseState

class MenuState():
    def __init__(self):
        #super().__init__(game)
        self.sub_menu = "MAIN"
        self.font = pygame.font.SysFont("Arial", 24)

        self.rects = {
            "start": pygame.Rect(400, 300, 220, 80),
            "tutorial": pygame.Rect(400, 380, 220, 80),
            "exit": pygame.Rect(400, 460, 220, 80),

            "create": pygame.Rect(242, 350, 220, 80),
            "join": pygame.Rect(562, 350, 220, 80),
            "back_arrow": pygame.Rect(20, 20, 60, 50)
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
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                    return
                    
            elif self.sub_menu == "ROOM_CHOICE":
                if self.rects.get("create") and self.rects["create"].collidepoint(event.pos):
                    send_queue.put(json.dumps({"action": "START_GAME"}))
                elif self.rects.get("join") and self.rects["join"].collidepoint(event.pos):
                    model.switch_to("JOIN_INPUT")
                elif self.rects.get("back_arrow") and self.rects["back_arrow"].collidepoint(event.pos):
                    self.sub_menu = "MAIN"
