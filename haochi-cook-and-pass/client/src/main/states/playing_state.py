import pygame
import random
from ..utilities import *
#import json
from .base_state import BaseState
#from ..templates import menu_view

class PlayingState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.ingredients = [] #ingredienti che il giocatore ha nella sua interfaccia di gioco 
        self.recipes = [[Ingredient('shrimp2.png', (30, 30), (0, 0), 1.5), Ingredient('ingred3.png', (30, 30), (0, 0), 3.5)], [Ingredient('lemon.png', (30, 30), (0, 0), 2.0)]]
        self.plate = Element("plate.png", (80, 80), (100, 100)) #lista di ricette del giocatore
        self.plate.set_plate()
        self.ingredients.append(Ingredient('ingred3.png', (100, 40), (10, 10), 3.5))
        self.ingredients.append(Ingredient('shrimp2.png', (50, 50), (300, 300), 1.5))
        self.ingredients.append(Ingredient("lemon.png", (70, 70), (200, 200), 2.0))
        self.score = 0.0
        self.current_recipe = [] #lista di ingredienti aggiunti nel piatto corrente per comporre la ricetta
        self.show_error_in_plate = False 
        self.new_ingredients = [] # lista di ingredienti inviati dai vicini o dalla cucina: tupla (Ingrediente, direzione) 
        self.recipe_complete = False #dice se la ricetta corrente è stata completata
        self.drag_not_next_ingredient = False #dice se viene trascinato un ingrediente che non è il prossimo della ricetta
        #campi per la gestione del timer
        self.cook_timer = None
        self.plate_time = 30
        self.passed_time = 0.0

        #faccio iniziare il timer
        self.start_game()

    def handle_input(self, event, send_queue, model):
        if event.type == pygame.QUIT:
            self.stop_clock()
            print("Chiudo il clock")
            running = False       
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.gestisci_pressione(pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEBUTTONUP:
            self.gestisci_rilascio()

    def start_game(self):
        self.cook_timer = CountdownThread(self.plate_time)
        self.cook_timer.start()    

    def gestisci_pressione(self, mouse_pos):
        for elem in [self.plate] + self.ingredients:
            #aggiorna il dragging a True per l'elemento
            elem.check_click(mouse_pos)
        #print("Premuto tasto")

    def gestisci_rilascio(self):
        for index, elem in enumerate(self.ingredients):
                elem.stop_dragging()
                if not elem.is_in_plate:
                    #se l'ingrediente si trova all'interno del piatto ma non è quello da inserire
                    if elem.detect_collision_plate(self.plate):
                        if self.recipes:
                            next_ingredient = self.get_next_ingredient()
                            if next_ingredient.name == elem.name:
                                elem.is_in_plate = True
                                elem.position = self.plate.position
                                elem.velocity = np.zeros(2)
                                #Si deve rimuovere dalla lista l'elemento in testa
                                self.recipes[0].pop(0)
                                #TO DO gestione del piatto completato, si abilita a mandarlo in cucina
                                self.current_recipe.append(self.ingredients.pop(index))
                        #self.plate.velocity = np.zeros(2)
        self.plate.stop_dragging()
        #print("Tasto rilasciato")  

    """Metodo per aggiornare tutti gli elementi del gioco"""
    def update(self, mouse_pos, screen_width, screen_height):
        #mouse_pos = pygame.mouse.get_pos()
        if self.cook_timer.curr_time >= self.cook_timer.clock_time:
            #il tempo è trascorso allora si deve rimuovere la lista della ricetta corrente e anche current_recipe
            self.cook_timer.reset_timer()
            self.passed_time = 0.0
            self.current_recipe = []
            self.recipes.pop(0)
            if len(self.recipes) == 0:
                print("Lo score del giocatore è: ", self.score)
                print("Il player ha finito le sue ricette, deve mandare un messaggino al server per avvisarlo che è in attesa anche se ancora può dover aspettare gli altri e passare ingredienti")
                #TO DO si chiude il timer
                self.stop_clock() 
                self.passed_time = 0.0
        else:    
            self.passed_time = round(self.cook_timer.curr_time, 1)
        print(self.passed_time)    
        #Aggiunta degli ingredienti inviati dal server (dalla cucina o dai vicini)
        for (ingr, side) in self.new_ingredients:
            if side == Side.LEFT:
                ingr.set_position(50, screen_height / 2)
                ingr.velocity = np.array([3.0, random.uniform(-3, 3)]) # Spinta verso l'interno
            elif side == Side.RIGHT:
                ingr.set_position(screen_width - 50, screen_height / 2) 
                ingr.velocity = np.array([-3.0, random.uniform(-3, 3)]) 
            elif side == Side.BOTTOM:
                ingr.set_position(screen_width / 2, screen_height)  
                ingr.velocity = np.array([random.uniform(-3, 3), 3.0])
            self.ingredients += [ingr]  

        self.new_ingredients = []      

        all_elements = self.ingredients + [self.plate]
        self.show_error_in_plate = False
        self.drag_not_next_ingredient = False
        next_ingr = self.get_next_ingredient()

        self.recipe_complete = len(self.recipes) > 0 and len(self.current_recipe) > 0 and len(self.recipes[0]) == 0
        player_ingredients = []

        for elem in all_elements:
            #if getattr(elem, "name", None):
            #    if elem.name == "lemon":
            #        print(f"Limone in posizione: {elem.position}")
            if elem == self.plate:
                elem.update_position(mouse_pos, screen_width, screen_height, can_exit_top = self.recipe_complete)
            else:    
                elem.update_position(mouse_pos, screen_width, screen_height)
                #se l'ingrediente è trascinato si setta a true self.drag_not_next_ingredient
                if next_ingr:
                    if elem.dragging and elem.name != next_ingr.name:
                        self.drag_not_next_ingredient = True
                else:
                   if elem.dragging:
                        self.drag_not_next_ingredient = True          
                #un ingrediente è stato passato ad un vicino
                if elem.position[0] < 0:
                    print("L'ingrediente è stato mandato al vicino sx")
                    #TO DO messaggino al server
                elif elem.position[0] > screen_width:
                    print("L'ingrediente è stato mandato al vicino dx")  
                    #TO DO messaggino al server
                else:
                    player_ingredients += [elem]
        #il piatto è stato inviato in cucina
        if self.plate.position[1] < 0:
            self.cook_timer.reset_timer()
            print("Il player avvisa forse il server o anche no")
            for ingr in self.current_recipe:
                self.score += ingr.score #AUMENTA LO SCORE del giocatore
            self.current_recipe = []
            self.recipes.pop(0)
            self.plate.set_position(screen_width * 1 / 3 ,screen_height * 2 / 3)
            self.plate.velocity = np.zeros(2)
            self.plate.dragging = False
            if len(self.recipes) == 0:
                print("Lo score del giocatore è: ", self.score)
                print("Il player ha finito le sue ricette, deve mandare un messaggino al server per avvisarlo che è in attesa anche se ancora può dover aspettare gli altri e passare ingredienti")
                #TO DO si chiude il timer
                self.stop_clock() 
                self.passed_time = 0.0
        #aggiornamento della lista corrente di ingredienti del giocatore, alcuni possono essere stati passati ai vicini
        all_elements = player_ingredients + [self.plate]
        self.ingredients = player_ingredients

         # 2. Gestione collisioni tra ingredienti (Fisica dei rimbalzi)
        for i in range(len(all_elements)):
            for j in range(i + 1, len(all_elements)):
                # Controlla collisione tra coppia i e j
                all_elements[i].check_collision_side(all_elements[j], next_ingr.name if next_ingr else None)
                all_elements[j].check_collision_side(all_elements[i], next_ingr.name if next_ingr else None)   
                #if all_elements[i].dragging:
                   # print("spostato")
                #Verifcica se l'ingrediente spostato non è il prossimo ingrediente della ricetta 
                if getattr(all_elements[i], "name", None) and all_elements[i].dragging:
                    if next_ingr is None or all_elements[i].name != next_ingr.name:
                        self.show_error_in_plate = True
                     #   print("Non è giusto")
        # 3. Mantieni gli ingredienti "cucinati" attaccati al piatto
        for ingr in self.current_recipe:
            ingr.position = self.plate.position       

    def get_next_ingredient(self):
        if self.recipes:
            if self.recipes[0]:
                return self.recipes[0][0]
        return None
    
    def add_new_ingredient(self, ingr_name, dimension, score, side): #dimension e score il server le prende dal DB
        added_ingr = Ingredient(ingr_name, dimension, (0, 0), score)
        #TO DO mettere posizione fittizia direttamente nel costruttore a None
        self.new_ingredients += [(added_ingr, side)]


    def stop_clock(self):
        self.cook_timer.running = False    

#
    #def draw(self, screen):
    #    menu_view.draw(screen, self.font, self.sub_menu, self.main_btn, self.create_btn, self.join_btn)