import pygame
from pathlib import Path
from .templates import menu_view, lobby_view, join_view

class GameView:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.SysFont("Arial", 24)
        self.code_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.base_path = Path(__file__).resolve().parent.parent.parent.parent

        #path immagini 
        path_home_bg=self.base_path/"images"/"home_background.jpg"

        raw_bg = pygame.image.load(str(path_home_bg)).convert()
        self.background = pygame.transform.scale(raw_bg, (width, height))

    def draw(self, model):
        #decide quale template disegnare in base allo stato attuale del modello
        state = model.current_state_key
        
        if state == "MENU":
            self.screen.blit(self.background, (0, 0))
            model.current_state.draw(self.screen)
        elif state == "LOBBY":
            #se sfondo diverso dal menu
            #self.screen.fill((240, 240, 240))
            lobby_view.draw(self.screen, model.game_code, self.font, self.code_font)
        elif state == "JOIN_INPUT":
            join_view.draw(self.screen, self.font, model.current_state.input_text)
        #todo aggiungere altri stati
        pygame.display.flip()