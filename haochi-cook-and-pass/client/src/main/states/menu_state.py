import pygame
import json
from .base_state import BaseState
from ..templates import menu_view

class MenuState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.sub_menu = "MAIN"
        self.main_btn = pygame.Rect(350, 250, 100, 50)
        self.create_btn = pygame.Rect(250, 250, 150, 50)
        self.join_btn = pygame.Rect(450, 250, 150, 50)
        self.font = pygame.font.SysFont("Arial", 24)

    def handle_input(self, event, send_queue, model):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.sub_menu == "MAIN":
                if self.main_btn.collidepoint(event.pos):
                    self.sub_menu = "ROOM_CHOICE"
            elif self.sub_menu == "ROOM_CHOICE":
                if self.create_btn.collidepoint(event.pos):
                    send_queue.put(json.dumps({"action": "START_GAME"}))
                elif self.join_btn.collidepoint(event.pos):
                    model.switch_to("JOIN_INPUT")

    def draw(self, screen):
        menu_view.draw(screen, self.font, self.sub_menu, self.main_btn, self.create_btn, self.join_btn)