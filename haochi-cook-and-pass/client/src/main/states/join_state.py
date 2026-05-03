import pygame
from .base_state import BaseState

class JoinState(BaseState):
    def __init__(self, model):
        super().__init__(model)
        self.input_text = ""

        self.rects = {
            "back_arrow": pygame.Rect(20, 20, 60, 50)
        }

    def handle_input(self, event, send_queue, model):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pygame.K_RETURN:
                # esempio: invia al server
                send_queue.put(self.input_text)
            else:
                self.input_text += event.unicode

    def update(self):
        pass