import pygame
import random
from ..utilities import *
import json
from .base_state import BaseState
#from ..templates import menu_view

class PlayingState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.ingredients = [] #ingredienti che il giocatore ha nella sua interfaccia di gioco 
        #Una ricetta è una terna (listaIngredienti, punteggio, tempoPerComporlo)
        self.recipes = []
        self.plate = Element("plate.PNG", (80, 80), (100, 100)) #lista di ricette del giocatore
        self.plate.set_plate()
        #self.ingredients.append(Ingredient('ingred3.PNG', (100, 40), (10, 10), 3.5))
        #self.ingredients.append(Ingredient('shrimp2.PNG', (50, 50), (300, 300), 1.5))
        #self.ingredients.append(Ingredient("lemon.PNG", (70, 70), (200, 200), 2.0))
        self.score = 0.0
        self.current_recipe = [] #lista di ingredienti aggiunti nel piatto corrente per comporre la ricetta
        self.current_time = 1
        self.show_error_in_plate = False 
        self.new_ingredients = [] # lista di ingredienti inviati dai vicini o dalla cucina: tupla (Ingrediente, direzione) 
        self.recipe_complete = False #dice se la ricetta corrente è stata completata
        self.drag_not_next_ingredient = False #dice se viene trascinato un ingrediente che non è il prossimo della ricetta
        #campi per la gestione del timer
        self.cook_timer = None
        #self.plate_time = 30
        self.passed_time = 0.0
        #Lista di messaggi da inviare al server
        self.send_msg = []
        #TO DO DA TOGLIERE solo per TEST!!!!!
        #self.add_starting_recipes([])
        #faccio iniziare il timer
        #self.start_game()

    def handle_input(self, event, send_queue, model):
        if event.type == pygame.QUIT:
            self.stop_clock()
            
            remaining = self.get_current_ingrendients()
            send_queue.put(json.dumps({
                "action": "QUIT_ROOM", 
                #Modificato
                #"ingrendients": remaining
            }))
            print("Chiudo il clock")
            running = False       
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_click(pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_release()

    def start_game(self):
        #sistemato
        #AGGIUNGI tempo richiesto per il primo piatto
        starting_time = self.recipes[0].time if self.recipes else 2000
        self.cook_timer = CountdownThread(starting_time)  #self.plate_time
        self.cook_timer.start()
#        print("Non è stato possibile settare il timer")    

    def handle_click(self, mouse_pos):
        for elem in [self.plate] + self.ingredients:
            #aggiorna il dragging a True per l'elemento
            elem.check_click(mouse_pos)
        #print("Premuto tasto")

    def handle_release(self):
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
                                self.recipes[0].ingredients.pop(0) #self.recipes[0].pop(0)
                                #TO DO gestione del piatto completato, si abilita a mandarlo in cucina
                                self.current_recipe.append(self.ingredients.pop(index))
                        #self.plate.velocity = np.zeros(2)
        self.plate.stop_dragging()
        #print("Tasto rilasciato")  

    """Metodo per aggiornare tutti gli elementi del gioco"""
    def update(self, mouse_pos, screen_width, screen_height):
        #mouse_pos = pygame.mouse.get_pos()
        #Si setta il primo timer se questo non era stato già fatto in start_game
        #DA RIMUOVERE UNA VOLTA CHE SARà COMPLETATO il METODO add_starting_recipes perchè lo start del timer viene fato lì
        #if self.recipes:
        #    if self.cook_timer.clock_time > self.recipes[0].time:
        #        self.cook_timer.reset_alarm_time(self.recipes[0].time)
        if self.cook_timer:
            current_timer_val = self.cook_timer.get_current_time()
            if current_timer_val >= self.cook_timer.clock_time:
                #il tempo è trascorso allora si deve rimuovere la lista della ricetta corrente e anche current_recipe
                print("TEMPO SCADUTO")
                self.cook_timer.reset_timer()
                self.passed_time = 0.0
                self.current_recipe = []
                if self.recipes:
                    self.recipes.pop(0)
                    #si aggiorna il timer
                    if self.recipes:
                        self.current_time = self.recipes[0].time #AGGIUNTO
                if len(self.recipes) == 0:
                    print("Lo score del giocatore è: ", self.score)
                    print("Il player ha finito le sue ricette, deve mandare un messaggino al server per avvisarlo che è in attesa anche se ancora può dover aspettare gli altri e passare ingredienti")
                    #TO DO si chiude il timer
                    self.stop_clock() 
                    self.passed_time = 0.0
                    #TO DO MODIFICA STATO ATTESA DEL GIOCATORE PER PASSARE A LIVELLO DOPO
                    self.send_msg += [CompletePlateMsg(self.current_recipe, 0.0, finished_all_plates = True)]
                else:
                    self.cook_timer.reset_alarm_time(self.recipes[0].time)  
            else:    
                self.passed_time = round(self.cook_timer.curr_time, 1)
        else:
            # il timer non esiste ancora
            current_timer_val = 0
            self.passed_time = 0.0            
            #print(self.passed_time)    
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
        next_ingr_name = next_ingr.name if next_ingr is not None else None #None se la lista è vuota
        self.send_msg = []

        self.recipe_complete = len(self.recipes) > 0 and len(self.current_recipe) > 0 and len(self.recipes[0].ingredients) == 0
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
                if elem.dragging:
                    if next_ingr_name is None or elem.name != next_ingr_name:
                        self.drag_not_next_ingredient = True          
                #un ingrediente è stato passato ad un vicino
                if elem.position[0] < 0:
                    print("L'ingrediente è stato mandato al vicino sx")
                    #TO DO messaggino al server
                    self.send_msg += [PassIngredientMsg(elem.name, Side.LEFT, elem.score, elem.dimension)]
                elif elem.position[0] > screen_width:
                    print("L'ingrediente è stato mandato al vicino dx")  
                    #TO DO messaggino al server
                    self.send_msg += [PassIngredientMsg(elem.name, Side.RIGHT, elem.score ,elem.dimension)]
                else:
                    player_ingredients += [elem]
        #il piatto è stato inviato in cucina
        if self.plate.position[1] < 0:
            self.cook_timer.reset_timer()
            #TO DO invio del messaggio al server per dire che un piatto è completato
            print("Il player avvisa forse il server o anche no")
            #CAMBIO GESTIONE SCORE per il momento lo si manda al server che aumenta lo score del giocatore
            plate_total_score = self.recipes[0].score #aggiunta
            #for ingr in self.current_recipe:
            #    total_score += ingr.score #calcolo del punteggio ottenuto dal piatto completato
            self.score += plate_total_score    
            if self.recipes:
                self.recipes.pop(0)
            if len(self.recipes) == 0:
                print("Lo score del giocatore è: ", self.score)
                print("Il player ha finito le sue ricette, deve mandare un messaggino al server per avvisarlo che è in attesa anche se ancora può dover aspettare gli altri e passare ingredienti")
                self.send_msg += [CompletePlateMsg(self.current_recipe.copy(), plate_total_score, finished_all_plates = True)]
                #TO DO si chiude il timer
                self.stop_clock() 
                self.passed_time = 0.0
            else: #caso inviato il piatto ma ce ne sono altri
                self.send_msg += [CompletePlateMsg(self.current_recipe.copy(), plate_total_score)]
                self.current_time = self.recipes[0].time #AGGIUNTI
                self.cook_timer.reset_alarm_time(self.recipes[0].time) #aggiunta
            #si passa al prossimo piatto              
            self.current_recipe = []
            self.plate.set_position(screen_width * 1 / 3 ,screen_height * 2 / 3)
            self.plate.velocity = np.zeros(2)
            self.plate.dragging = False
            
        #aggiornamento della lista corrente di ingredienti del giocatore, alcuni possono essere stati passati ai vicini
        all_elements = player_ingredients + [self.plate]
        self.ingredients = player_ingredients

         # 2. Gestione collisioni tra ingredienti (Fisica dei rimbalzi)
        for i in range(len(all_elements)):
            for j in range(i + 1, len(all_elements)):
                # Controlla collisione tra coppia i e j
                all_elements[i].check_collision_side(all_elements[j], next_ingr_name)
                all_elements[j].check_collision_side(all_elements[i], next_ingr_name)   
                #if all_elements[i].dragging:
                   # print("spostato")
                #Verifcica se l'ingrediente spostato non è il prossimo ingrediente della ricetta 
                if getattr(all_elements[i], "name", None) and all_elements[i].dragging:
                    if next_ingr is None or all_elements[i].name != next_ingr.name:
                        self.show_error_in_plate = True
                     #   print("Non è giusto")
        # 3. Mantieni gli ingredienti "cucinati" attaccati al piatto
        for ingr in self.current_recipe:
            ingr.position = self.plate.position #copia del vettore indipendente     

        return self.send_msg      

#sistemato
    def get_next_ingredient(self):
        if self.recipes and self.recipes[0].ingredients:
                return self.recipes[0].ingredients[0]
        return None
    
    #metodo per aggiungere ingredienti mandati da altri utenti
    def add_new_ingredient(self, ingr_name, dimension, score, side): #dimension e score il server le prende dal DB
        dimension_np = np.array([float(dimension[0]), float(dimension[1])])
        added_ingr = Ingredient(ingr_name, dimension_np, (0, 0), score)
        #TO DO mettere posizione fittizia direttamente nel costruttore a None
        self.new_ingredients += [(added_ingr, Side[side])]

    def stop_clock(self):
        self.cook_timer.running = False    
        print(self.cook_timer.running)

    #metodo per aggiungere una lista di ingredienti all'inizio del livello
    def add_starting_ingredients(self, list_ingredients):
        print(f"Ricevuta la seguente lista di ingredienti {list_ingredients}")
        #for (ingr_name, dimension, score) in list_ingredients:
        #    self.add_new_ingredient(ingr_name, dimension, score, "BOTTOM")
        for ingr in list_ingredients:
            self.add_new_ingredient(f"{ingr}.PNG", (50, 50), 0, "BOTTOM")

#sistemare
    #metodo per settare la lista di piatti all'inizio del livello invocato quando arriva la lista di ricette dal server
    def add_starting_recipes(self, list_recipes): #list_recipes formata da lista di ricette dove ogni ricetta ha lista (nome_igr, dimensione, score), score e time
        print(f"Ricevuta la seguente lista di ricette {list_recipes}")
        for recipe in list_recipes:
            list_ingredients = []
            for ingr in recipe["ingredients"]:
                list_ingredients.append(Ingredient(f"{ingr}.PNG", (30, 30), (0, 0), 0))
            self.recipes.append(Recipe(list_ingredients, recipe["time"], recipe["points"]))
        self.current_time = self.recipes[0].time #AGGIUNTO   
        #Quando si passa al livello successivo si rimuovono tutti gli ingredienti del livello precedente
        self.ingredients = [] 
        #si fa iniziare il timer
        self.start_game()     
        #TEST
        #self.recipes = [Recipe([Ingredient('shrimp2.PNG', (30, 30), (0, 0), 1.5), Ingredient('ingred3.PNG', (30, 30), (0, 0), 3.5)], 270, 20), Recipe([Ingredient('lemon.PNG', (30, 30), (0, 0), 2.0)], 240, 5)]
        #si fa iniziare il timer
        #self.start_game() 
    #def draw(self, screen):
    #    menu_view.draw(screen, self.font, self.sub_menu, self.main_btn, self.create_btn, self.join_btn)'''' #for (ingr_name, dimension, score) in list_plates:
        #    self.recipes.append(Ingredient(ingr_name + ".png", dimension, (0, 0) , score))
        '''for recipe in list_recipes:
            list_ingredients_in_recipe = []
            for ingr in self.ingredients:
                list_ingredients_in_recipe.append(Ingredient(ingr_name + ".png", dimension, (0, 0) , score))
            self.recipes.append(Recipe)'''

    def get_current_ingrendients(self):
        return [ingr.name.removesuffix(".PNG") for ingr in self.ingredients]