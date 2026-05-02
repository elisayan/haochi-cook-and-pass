import pygame
from .templates import menu_view, lobby_view, join_view, play_view
from pathlib import Path

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
            #TO DO rimuovere
            model.game_code = "1234"
            model.ingr_id = "shrimp" 
            lobby_view.draw(self.screen, model.game_code, model.ingr_id, model.current_state.ready_players, model.current_state.is_starting_player, self.font, self.code_font, model.current_state.circle, model.current_state.plates, model.current_state.start_btn, model.current_state.quit_btn)
        elif state == "JOIN_INPUT":
            join_view.draw(self.screen, self.font, model.current_state.input_text)
        elif state == "PLAYING":
            model = model.current_state
            #si prende il prossimo elemento da dover inserire nel piatto
            next_ingredient = None
            if len(model.recipes) > 0:
                if model.recipes[0]:
                    next_ingredient = model.recipes[0][0]
                    next_ingredient.set_position(self.screen.get_width() / 2, next_ingredient.dimension[1] / 2)
            #calcolo della rotazione della lancetta
            tick_rotation = (model.passed_time / model.plate_time) * 360

            play_view.draw_game(self.screen,
                                model.plate, 
                                model.ingredients, 
                                model.current_recipe, 
                                next_ingredient, 
                                model.show_error_in_plate, 
                                model.score,
                                model.recipe_complete,
                                model.drag_not_next_ingredient, 
                                tick_rotation)   
        #todo aggiungere altri stati
        pygame.display.flip()