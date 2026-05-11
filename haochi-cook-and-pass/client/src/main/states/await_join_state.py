import pygame
import json
from .base_state import BaseState

class AwaitJoinState(BaseState):
    def __init__(self, model):
        super().__init__(model)

        self.rects = {
            "back_arrow": pygame.Rect(20, 20, 60, 50)
        }

    def handle_input(self, event, send_queue, model):
        #todo deve solo aspettare che il host della stanza avvia il gioco
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rects["back_arrow"].collidepoint(event.pos):
                model.switch_to("MENU")
                send_queue.put(json.dumps({"action": "QUIT_ROOM"}))

    def update(self, mouse_pos, screen_width, screen_height):
        pass
    