import pygame
from pathlib import Path

class GameView:
    def __init__(self, width=800, height=400):
        pygame.init() #inizializzazione del motore Pygame
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height)) #finestra di gioco
        pygame.display.set_caption('Haochi')
        
        # Caricamento risorse grafiche
        self.test_font = pygame.font.Font(None, 50)
        path_bg = Path(__file__).resolve().parent.parent / "images" / "Background.png"
        self.background = pygame.image.load(str(path_bg)).convert_alpha()
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

    def draw_game(self, plate, list_elem, current_recipe):#, list_recipe):
        """Metodo che si occupa unicamente di renderizzare"""
        # Sfondo
        self.screen.blit(self.background, (0, 0))
        
        # Ingredienti e Piatto
        for elem in [plate] + list_elem + current_recipe:
            surface = pygame.image.load(str(elem.path)).convert_alpha()
            surface = pygame.transform.scale(surface, elem.dimension).convert_alpha()
            # Calcoliamo l'angolo in alto a sinistra partendo dal centro (position)
            top_left_x = elem.position[0] - elem.dimension[0] / 2
            top_left_y = elem.position[1] - elem.dimension[1] / 2
            
            # DISEGNO: primo argomento è l'immagine, secondo è la coordinata (x, y)
            self.screen.blit(surface, (top_left_x, top_left_y))
            
        # Ingredienti già nel piatto (la ricetta)
        #for ingr in list_recipe:
        #    surface = pygame.image.load(str(ingr.path)).convert_alpha()
        #    surface = pygame.transform.scale(surface, ingr.dimension).convert_alpha()
        #    self.screen.blit(surface, ingr.rect)
            
        # Aggiornamento display
        pygame.display.update()

    def get_events(self):
        """Traduce gli eventi Pygame in un formato neutro"""
        events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                events.append({"type": "QUIT"})
            elif event.type == pygame.MOUSEBUTTONDOWN:
                events.append({
                    "type": "CLICK", 
                    "pos": event.pos, 
                    "button": event.button
                })
            elif event.type == pygame.MOUSEBUTTONUP:
                events.append({"type": "RELEASE"})
        return events

    def get_mouse_pos(self):
        """Restituisce le coordinate (x, y) attuali del mouse"""
        return pygame.mouse.get_pos()