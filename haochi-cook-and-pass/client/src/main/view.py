import pygame
from .templates import menu_view, lobby_view, join_view, play_view
from pathlib import Path

class GameView:
    def __init__(self, width=1024, height=576):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.font = pygame.font.SysFont("Arial", 24)
        self.code_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.base_path = Path(__file__).resolve().parent.parent.parent.parent

        #path immagini 
        self.start_img = self.load_img("start_button.png")
        self.tutorial_img = self.load_img("tutorial_button.png")
        self.exit_img = self.load_img("exit_button.png")
        self.home_bg = pygame.transform.smoothscale(self.load_img("homepage.jpg", alpha=False), (width, height))
        self.room_choice_bg = pygame.transform.smoothscale(self.load_img("background.jpg", alpha=False), (width, height))

    def load_img(self, name, alpha=True):
        path = self.base_path / "images" / name
        img = pygame.image.load(str(path))
        return img.convert_alpha() if alpha else img.convert()

    def draw(self, model):
        #decide quale template disegnare in base allo stato attuale del modello
        state = model.current_state_key
        
        if state == "MENU":
            if model.current_state.sub_menu == "MAIN":
                self.screen.blit(self.home_bg, (0, 0))
            elif model.current_state.sub_menu == "ROOM_CHOICE":
                self.screen.blit(self.room_choice_bg, (0, 0))
                
            rects = menu_view.draw(
                self.screen,
                self.font,
                model.current_state.sub_menu,
                model.current_state.create_btn,
                model.current_state.join_btn,
                self.start_img,
                self.tutorial_img,
                self.exit_img
            )
            model.current_state.rects = rects
        elif state == "LOBBY":
            #se sfondo diverso dal menu
            #self.screen.fill((240, 240, 240))
            lobby_view.draw(self.screen, model.game_code, self.font, self.code_font)
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