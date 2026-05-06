import pygame
import json
from .base_state import BaseState

class JoinState(BaseState):
    def __init__(self, model):
        super().__init__(model)
        self.input_text = ""
        self.max_length = 4

        self.card_rect = pygame.Rect(0, 0, 500, 350)
        self.join_btn_rect = pygame.Rect(0, 0, 150, 45)

        self.rects = {
            "back_arrow": pygame.Rect(20, 20, 60, 50)
        }

    def handle_input(self, event, send_queue, model):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rects["back_arrow"].collidepoint(event.pos):
                model.switch_to("MENU")
            elif self.join_btn_rect.collidepoint(event.pos) and self.input_text:
                send_queue.put(json.dumps({"action": "JOIN_ROOM", "code": self.input_text}))
                print("JOIN ROOM CON CODICE:", self.input_text)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                model.switch_to("MENU")
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pygame.K_RETURN:
                send_queue.put(json.dumps({"action": "JOIN_ROOM", "code": self.input_text}))
                print("JOIN ROOM CON CODICE:", self.input_text)
            else:
                if len(self.input_text) < self.max_length:
                    self.input_text += event.unicode

    def update(self, mouse_pos, screen_width, screen_height):
        self.card_rect.center = (screen_width // 2, screen_height // 2)
        self.join_btn_rect.center = (screen_width // 2, self.card_rect.bottom - 50)