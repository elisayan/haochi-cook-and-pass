from pathlib import Path
import numpy as np

braking = 0.01

class Element ():
    def __init__(self, image_name, dimension:tuple, position):
        self.path = Path(__file__).resolve().parent.parent / "main" / "images" / image_name
        self.dimension = dimension #la dimensione è immutabile
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

    def update_position(self, mouse_pos, screen_width, screen_height):
        """Metodo per aggiornare la posizione se l'oggetto è cliccato e trascinato"""
        if self.dragging:
            self.position = np.array([float(mouse_pos[0]), float(mouse_pos[1])])
        
        # --- CONTROLLO BORDI ---
        width, height = self.dimension
        half_w, half_h = width / 2, height / 2

        # Rimbalzo X
        if self.position[0] - half_w < 0:
            self.position[0] = half_w
            self.velocity[0] *= -1
        elif self.position[0] + half_w > screen_width:
            self.position[0] = screen_width - half_w
            self.velocity[0] *= -1

        # Rimbalzo Y
        if self.position[1] - half_h < 0:
            self.position[1] = half_h
            self.velocity[1] *= -1
        elif self.position[1] + half_h > screen_height:
            self.position[1] = screen_height - half_h
            self.velocity[1] *= -1

        # Attrito per rallentare la velocità NON VA ???
        for i in range(2):
            if abs(self.velocity[i]) > 0:
                prev_sign = np.sign(self.velocity[i])
                self.velocity[i] -= prev_sign * braking
                # Se abbiamo superato lo zero, fermiamolo
                if np.sign(self.velocity[i]) != prev_sign:
                    self.velocity[i] = 0.0 

    """Individua le collisioni tra elementi e li sposta o la collisione tra piatto ed elemento se quest'ultimo non è il successivo ingradietne da inserire nel piatto ??? TO DO"""
    def check_collision_side(self, other_element):
    # REGOLA 1: Se uno dei due è il piatto, NON fare nulla qui.
    # La collisione col piatto la gestiamo solo nel 'gestisci_rilascio'.
        if self.is_plate or other_element.is_plate:
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

class Ingredient(Element):
    def __init__(self, image_name, dimension:tuple, position):
        super().__init__(image_name, dimension, position)
        self.is_in_plate = False
        self.name = image_name.removesuffix('.png')

    def check_collision_side(self, other_elem):
        # Se l'ingrediente NON è nel piatto, esegui la logica di rimbalzo del genitore
        if not self.is_in_plate:
            return super().check_collision_side(other_elem)
        
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
            self.is_in_plate = True
            self.position = plate.position
            self.velocity = np.zeros(2)
            print(f'Ingrediente {self.name} è nel piatto')

