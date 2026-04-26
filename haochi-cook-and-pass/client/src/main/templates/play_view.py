import pygame
from pathlib import Path

def draw_game(screen, plate, list_elem, current_recipe, next_ingredient, show_error, score, show_to_arrow, show_left_right_arrows, tick_rotation):
        """Metodo che si occupa unicamente di renderizzare"""
        width = screen.get_width()
        height = screen.get_height()
        # Sfondo
        path_bg = Path(__file__).resolve().parent.parent / "images" / "Background.png"
        background = pygame.image.load(str(path_bg)).convert_alpha()
        background = pygame.transform.scale(background, (width, height)) 
        screen.blit(background, (0, 0))
        
        path_arrow = Path(__file__).resolve().parent.parent / "images" / "arrow.png"
        #Freccia in alto per indicare di mandare il piatto in cucina
        if show_to_arrow:
            _render_element(screen, path_arrow, [width / 2, 50], [80, 80])

        if show_left_right_arrows:
            _render_element(screen, path_arrow, [width - 50, height / 2], [80, 80], -90)
            _render_element(screen, path_arrow, [50, height / 2], [80, 80], 90)

        path_clock = Path(__file__).resolve().parent.parent / "images" / "clock1.png"
        # Posizione: [40, 40], Dimensione: [50, 50]
        _render_element(screen, path_clock, [40, 40], [50, 50])

        path_tick = Path(__file__).resolve().parent.parent / "images" / "clock2.png"
        # Lancetta (Tick)
        # Posizione: DEVE ESSERE LA STESSA [40, 40] per ruotare sul centro dell'orologio
        # Dimensione: [8, 30] (larghezza 8, altezza 30 per non uscire dal bordo)
        _render_element(screen, path_tick, [40, 40], [8, 14], -tick_rotation, [2, -5])

        #Si renderizza solo il primo ingrediente del piatto corrente in alto al centro
        if next_ingredient:
            padding = 20
            # Rettangolo per il background del prossimo ingrediente da inserire
            bg_rect = pygame.Rect(0, 0, next_ingredient.dimension[0] + padding, 
                                    next_ingredient.dimension[1] + padding)
            bg_rect.center = next_ingredient.position
            
            # Rettangolo bianco con bordi arrotondati (raggio 10)
            pygame.draw.rect(screen, (255, 255, 255), bg_rect, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), bg_rect, width=1, border_radius=10)
            _render_element(screen, next_ingredient.path, next_ingredient.position, next_ingredient.dimension)
         
        #next_ingredient = []

        #  Ingredienti e Piatto
        for elem in [plate] + list_elem + current_recipe:
            _render_element(screen, elem.path, elem.position, elem.dimension)

        #Inserimento della X rossa nel piatto
        if show_error:
            path_error = Path(__file__).resolve().parent.parent / "images" / "error.png"
            scale_factor = 0.7
            _render_element(screen, path_error, plate.position, plate.dimension * scale_factor)
            #surface = pygame.image.load(str(self.path_error)).convert_alpha()
            
           # surface = pygame.transform.scale(surface, plate.dimension * scale_factor).convert_alpha()
            # Calcoliamo l'angolo in alto a sinistra partendo dal centro (position)
            #top_left_x = plate.position[0] - (plate.dimension[0] * scale_factor) / 2
            #top_left_y = plate.position[1] - (plate.dimension[1] * scale_factor) / 2
            
            # DISEGNO: primo argomento è l'immagine, secondo è la coordinata (x, y)
            #self.screen.blit(surface, (top_left_x, top_left_y))
        draw_score(screen, score, width)    
        # 4. Aggiornamento display
        pygame.display.update()

def draw_score(screen, score, width):
    font = pygame.font.SysFont("Arial", 30, bold=True)
    score_surface = font.render(f"Score: {score:.1f}", True, (50, 50, 50)) # Testo grigio scuro
    
    # Posizionamento a 20 pixel dal bordo destro e superiore
    margin = 20
    x_pos = width - score_surface.get_width() - margin
    screen.blit(score_surface, (x_pos, margin))    

def _render_element(screen, path, position, dimension, rotation = 0, pivot_offset = None):
    # 1. Caricamento e scalatura
    surface = pygame.image.load(str(path)).convert_alpha()
    surface = pygame.transform.scale(surface, dimension)
    
    if rotation != 0:
        # 2. Rotazione della superficie
        surface = pygame.transform.rotate(surface, rotation)
        
        if pivot_offset is not None:
            # CONDIZIONE PIVOT: Calcoliamo lo sfasamento del centro
            # Dobbiamo ruotare il vettore offset della stessa quantità
            offset = pygame.math.Vector2(pivot_offset)
            # Ruotiamo l'offset (Pygame ruota in senso antiorario, quindi usiamo -rotation)
            offset_rotated = offset.rotate(-rotation)
            
            # Il nuovo centro sarà la posizione desiderata + l'offset ruotato
            rect = surface.get_rect(center=pygame.math.Vector2(position) + offset_rotated)
        else:
            # Rotazione standard centrata
            rect = surface.get_rect(center=position)
    else:
        # 3. Nessuna rotazione: calcolo standard
        rect = surface.get_rect(center=position)
    
    # 4. Disegno finale
    screen.blit(surface, rect.topleft)