from utilities import *

class Client():
    def __init__(self):
        self.ingredients = []
        self.recipes = []
        self.plate = Element("plate.png", (80, 80), (100, 100))
        self.plate.set_plate()
        self.ingredients.append(Ingredient('ingred3.png', (100, 40), (10, 10)))
        self.ingredients.append(Ingredient('shrimp2.png', (50, 50), (300, 300)))
        self.score = 0
        self.current_recipe = [] #lista di ingradienti

    def gestisci_pressione(self, mouse_pos):
        for elem in [self.plate] + self.ingredients:
            #aggiorna il dragging a True per l'elemento
            elem.check_click(mouse_pos)
        print("Premuto tasto")

    def gestisci_rilascio(self):
        for index, elem in enumerate(self.ingredients):
                elem.stop_dragging()
                if not elem.is_in_plate:
                    elem.detect_collision_plate(self.plate)
                    if elem.is_in_plate:
                        self.current_recipe.append(self.ingredients.pop(index))
                        #self.plate.velocity = np.zeros(2)
        self.plate.stop_dragging()
        print("Tasto rilasciato")  

    """Metodo per aggiornare tutti gli elementi del gioco"""
    def update(self, mouse_pos, screen_width, screen_height):
        all_elements = [self.plate] + self.ingredients

        for elem in all_elements:
            elem.update_position(mouse_pos, screen_width, screen_height)

         # Gestione collisioni tra ingredienti (Fisica dei rimbalzi)
        for i in range(len(all_elements)):
            for j in range(i + 1, len(all_elements)):
                # Controlla collisione tra coppia i e j
                all_elements[i].check_collision_side(all_elements[j])
                all_elements[j].check_collision_side(all_elements[i])   

        # 3. Mantieni gli ingredienti "cucinati" attaccati al piatto
        for ingr in self.current_recipe:
            ingr.position = self.plate.position.copy()        
