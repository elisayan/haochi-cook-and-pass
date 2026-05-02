from pathlib import Path
import numpy as np
import threading
from time import sleep

from enum import Enum, auto

class Side(Enum):
    LEFT = auto()
    RIGHT = auto()
    BOTTOM = auto()

class Element ():
    def __init__(self, image_name, dimension:tuple, position):
        self.path = Path(__file__).resolve().parent / "images" / image_name
        self.dimension = np.array([float(dimension[0]), float(dimension[1])])
        self.position = np.array([float(position[0]), float(position[1])])
        self.dragging = False
        self.velocity = np.zeros(2) #np.array([0.0, 0.0])
        self.is_plate = False

    def set_plate(self):
        self.is_plate = True    

    def get_boundaries(self):
        """Metodo per ottenere left, right, top, bottom"""
        w, h = self.dimension
        return (self.position[0] - w/2, self.position[0] + w/2, 
                self.position[1] - h/2, self.position[1] + h/2)

    def check_click(self, mouse_pos): 
        """Metodo che verifica se il mouse è stato cliccato sull'elemento"""
        # Simulo l'area del rettangolo a partire dal suo centro e dalla sua dimensione
        left, right, top, bottom = self.get_boundaries()

        if left <= mouse_pos[0] <= right and top <= mouse_pos[1] <= bottom:
            self.dragging = True 
    
    
    def stop_dragging(self):
        """Metodo che setta dragging dell'elemento a false"""
        self.dragging = False

    def update_position(self, mouse_pos, screen_width, screen_height, can_exit_top = False):
        """Metodo per aggiornare la posizione se l'oggetto è cliccato e trascinato"""
        friction = 0.92 
        abs_limit_velocity = 20.0

        if self.dragging:
            new_position = np.array([float(mouse_pos[0]), float(mouse_pos[1])])
            # La velocità è lo spostamento del mouse
            self.velocity = new_position - self.position 
            self.position = new_position
        else: 
            #Si muove l'oggetto della sua velocità attuale
            self.position += self.velocity
            
            # Si applica l'attrito per ridurre la velocità
            self.velocity *= friction
            
            # Se l'elemento si muove piano si ferma
            if np.linalg.norm(self.velocity) < 0.2:
                self.velocity = np.zeros(2)

        # 4. Limita la velocità massima (Cap)
        speed = np.linalg.norm(self.velocity)
        if speed > abs_limit_velocity:
            self.velocity = (self.velocity / speed) * abs_limit_velocity # la prima divisione mantiene il vettore unitario della direzione dell'elemento 

        # --- CONTROLLO BORDI ---
        width, height = self.dimension
        half_w, half_h = width / 2, height / 2

        # Rimbalzo X
        if self.is_plate:
            if self.position[0] - half_w < 0:
                self.position[0] = half_w
                self.velocity[0] *= -1
            elif self.position[0] + half_w > screen_width:
                self.position[0] = screen_width - half_w
                self.velocity[0] *= -1

        # Rimbalzo Y
        # tiro verso l'alto, se il current_recipe non è vuoto e recipes[0] è vuoto 
        # allora si permette al piatto di essere mandato alla cucina
        if self.position[1] - half_h < 0:
            if not can_exit_top:
                self.position[1] = half_h
                self.velocity[1] *= -1    
        elif self.position[1] + half_h > screen_height:
            self.position[1] = screen_height - half_h
            self.velocity[1] *= -1

    """Individua le collisioni tra elementi e li sposta o la collisione tra piatto ed elemento se quest'ultimo non è il successivo ingradietne da inserire nel piatto ??? TO DO"""
    def check_collision_side(self, other_element, next_ingredient_name = None):
    # se uno dei due è il piatto, allora si verifica se l'ingrediente ha diritto di stare nel piatto
        if self.is_plate or other_element.is_plate:
            ingr = other_element if self.is_plate else self

            #se l'ingrediente è il prossimo richiesto dalla ricetta allora non si verifica la collisione fisica
            if getattr(ingr, "name", None) and ingr.name == next_ingredient_name:
                return

        # REGOLA 2: Se l'ingrediente è già nel piatto, non deve più scontrarsi con gli altri
        if getattr(self, 'is_in_plate', False):
            return
    # Verifichiamo se c'è effettivamente una collisione
        l1, r1, t1, b1 = self.get_boundaries()
        l2, r2, t2, b2 = other_element.get_boundaries()

        # Verifica se c'è sovrapposizione 
        if r1 > l2 and l1 < r2 and b1 > t2 and t1 < b2:
            overlap_sx = r1 - l2
            overlap_dx = r2 - l1
            overlap_up = b1 - t2
            overlap_dw = b2 - t1

            min_overlap = min(overlap_sx, overlap_dx, overlap_up, overlap_dw)

            #NON VA ??? TO DO
            # Logica dei rimbalzi identica alla tua, ma usando self.velocity[0] e [1]
            # Spostiamo l'oggetto fuori dalla collisione immediatamente
            if min_overlap == overlap_sx:
                if not self.dragging: self.position[0] -= min_overlap
                if not other_element.dragging: other_element.position[0] += min_overlap
                self.velocity[0] *= -0.5 # Rimbalzo leggero
            elif min_overlap == overlap_dx:
                if not self.dragging: self.position[0] += min_overlap
                if not other_element.dragging: other_element.position[0] -= min_overlap
                self.velocity[0] *= -0.5
            elif min_overlap == overlap_up:
                if not self.dragging: self.position[1] -= min_overlap
                if not other_element.dragging: other_element.position[1] += min_overlap
                self.velocity[1] *= -0.5
            elif min_overlap == overlap_dw:
                if not self.dragging: self.position[1] += min_overlap
                if not other_element.dragging: other_element.position[1] -= min_overlap
                self.velocity[1] *= -0.5

    def set_position(self, x, y):
        self.position = np.array([float(x), float(y)])            

class Ingredient(Element):
    def __init__(self, image_name, dimension:tuple, position, score):
        super().__init__(image_name, dimension, position)
        self.is_in_plate = False
        self.name = image_name.removesuffix('.png')  
        self.score = score

    def check_collision_side(self, other_elem, next_ingredient_name = None):
        # Se l'ingrediente NON è nel piatto, esegui la logica di rimbalzo del genitore
        if not self.is_in_plate:
            return super().check_collision_side(other_elem, next_ingredient_name)
        
        # Se è nel piatto, non chiamiamo il genitore (l'ingrediente resta fermo)
        return None
    
    def inside(self, plate):
        #Verifica se l'ingrediente è all'interno del piatto
        l1, r1, t1, b1 = self.get_boundaries()
        l2, r2, t2, b2 = plate.get_boundaries()
        
        if r1 > l2 and l1 < r2 and b1 > t2 and t1 < b2:
            return True
    
        return False

    def detect_collision_plate(self, plate):
        #Aggiorna lo stato (posizione e is_in_plate) dell'ingradiete se entra nel piatto
        if self.inside(plate):
           # self.is_in_plate = True
           # self.position = plate.position
           # self.velocity = np.zeros(2)
            print(f'Ingrediente {self.name} è nel piatto')
            return True
        return False
    
class Player_Id(Ingredient):
    def __init__(self, image_name, dimension:tuple, original_pos, position = (0, 0), score = 0.0):
        super().__init__(image_name, dimension, position, score)   
        self.is_in_plate = False
        self.original_pos = np.array([float(original_pos[0]), float(original_pos[1])])
        self.position = self.original_pos.copy()
    
import threading
from time import sleep

#Thread che viene lanciato parallelamente al gioco per gestire il passare del tempo per comporre ad inviare il piatto corrente
class CountdownThread(threading.Thread):
    def __init__(self, clock_time):
        super().__init__()
        self.curr_time = 0.0
        self.clock_time = clock_time #TO CHANGE clock time non serve +
        # Flag per fermare il thread in modo pulito se necessario
        self.running = True 

    def run(self):
#comportamento del thread è quello di attendere 0.1 secondi e poi aggiornare il valore 
        while self.running:
            sleep(0.1)
            self.curr_time += 0.1
    def get_current_time(self):
        """Ritorna il valore attuale del timer"""
        return round(self.curr_time, 1)
    
    def reset_timer(self):
        self.curr_time = 0.0

class PartialMessage():
    pass

class PassIngredientMsg(PartialMessage):
    def __init__(self, ingr_name, direction, score, dimension):
        #si crea un dizionario che è il messaggio parziale che deve essere inviato
        self.msg = {
            "ingr_name": ingr_name,
            "direction": direction.name, #conversion of Side... in string
            "score": score,
            "dimension": dimension.tolist(), #converion of numpy array to List
            "action": "PASS_INGREDIENT"
        }

class CompletePlateMsg(PartialMessage):
    def __init__(self, list_ingr, total_score, finished_all_plates = False):
        list_names = []
        for ingr in list_ingr:
            list_names.append(ingr.name)
        self.msg = {
            "completed_plate": list_names,
            "finished_all_plates": finished_all_plates,
            "gained_score": total_score,
            "action": "PLATE_COMPLETE"
        }
        

