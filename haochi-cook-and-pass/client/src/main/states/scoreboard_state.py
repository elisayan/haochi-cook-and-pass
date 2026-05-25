import pygame
from .base_state import BaseState

class ScoreboardState(BaseState):
    def __init__(self, model):
        super().__init__(model)
        self.rects = {
            "home_btn": pygame.Rect(0, 0, 160, 45)
        }
        self.scores = {
            "player": {"name": "", "dishes": 0, "points": 0},
            "team": {"dishes": 0, "points": 0}
        }

    def handle_input(self, event, send_queue, model):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rects.get("home_btn") and self.rects["home_btn"].collidepoint(event.pos):
                model.set_state("MENU")