import pygame
from .templates import menu_view, lobby_view, join_view

class GameView:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.SysFont("Arial", 24)
        self.code_font = pygame.font.SysFont("Arial", 48, bold=True)

    def draw(self, model):
        #decide quale template disegnare in base allo stato attuale del modello
        state = model.current_state_key
        
        if state == "MENU":
            model.current_state.draw(self.screen)
        elif state == "LOBBY":
            lobby_view.draw(self.screen, model.game_code, self.font, self.code_font)
        elif state == "JOIN_INPUT":
            join_view.draw(self.screen, self.font, model.current_state.input_text)
        #todo aggiungere altri stati
        pygame.display.flip()