import pygame
import json
from .base_state import BaseState
from ..templates import menu_view

class MenuState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.sub_menu = "MAIN"
        #self.main_btn = pygame.Rect(350, 250, 100, 50)
        self.create_btn = pygame.Rect(250, 250, 150, 50)
        self.join_btn = pygame.Rect(450, 250, 150, 50)
        self.font = pygame.font.SysFont("Arial", 24)

        self.rects = {}

    def handle_input(self, event, send_queue, model):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.rects:
                return

            if self.sub_menu == "MAIN":
                if self.rects["start"].collidepoint(event.pos):
                    self.sub_menu = "ROOM_CHOICE"
                elif self.rects["tutorial"].collidepoint(event.pos):
                    print("TUTORIAL")
                elif self.rects["exit"].collidepoint(event.pos):
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
            elif self.sub_menu == "ROOM_CHOICE":
                if self.rects.get("create") and self.rects["create"].collidepoint(event.pos):
                    send_queue.put(json.dumps({"action": "START_GAME"}))
                elif self.rects.get("join") and self.rects["join"].collidepoint(event.pos):
                    model.switch_to("JOIN_INPUT")

    def draw(self, screen, start_img, tutorial_img, exit_img):
        self.rects = menu_view.draw(
            screen,
            self.font,
            self.sub_menu,
            self.create_btn,
            self.join_btn,
            start_img,
            tutorial_img,
            exit_img
        )