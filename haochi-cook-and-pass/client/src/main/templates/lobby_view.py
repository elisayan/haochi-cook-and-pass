"""pagina di attesa di un segnale Start dal server"""
import pygame
import math
from pathlib import Path

def draw(screen, game_code, player_id, players_id, is_starting_player, font, code_font, circle, plates, start_btn, quit_btn):
    screen.fill((255, 255, 102))
    width = screen.get_width()
    height = screen.get_height()
    label = font.render("Room Code:", True, (0, 0, 0))
    code_text = code_font.render(game_code, True, (0, 0, 255))
    screen.blit(label, (80, 30))
    screen.blit(code_text, (80, 55))
    quit_btn = pygame.Rect(80, 500, 100, 50)
    pygame.draw.rect(screen, (255, 165, 0), quit_btn)
    text = font.render("QUIT", True, (255, 255, 255))
    screen.blit(text, (quit_btn.x + 25, quit_btn.y + 10))
    if is_starting_player:
        #start_btn = pygame.Rect(620, 500, 100, 50)
        pygame.draw.rect(screen, (0, 255, 0), start_btn)
        text = font.render("START", True, (255, 255, 255))
        screen.blit(text, (start_btn.x + 20, start_btn.y + 10))
        #center = (width/2 + 100, height/2 - 40)
        #radius = 200
        center = circle[0]
        radius = circle[1]
        pygame.draw.circle(screen, (0, 0, 0), center, radius, 2)
        """positions = _get_circle_positions(center, radius, num_circles = 8)
        for pos in positions:
            #pygame.draw.circle(screen, (0, 0, 0), pos, 30, 2)
            plate_scale = 100
            _render_player_id(screen, "plate", (pos[0] - plate_scale/2, pos[1] - plate_scale/2), (plate_scale, plate_scale))
        """
        i = 0
        for plate in plates:
            _render_player_id(screen, "plate", plate.position, plate.dimension, render_number = True, number = i)
            i += 1
            """print("posizione:", plate.position)
            print("dimensione:",plate.dimension)
            print()"""
        """starting_sx_pos = 50
        starting_height = 30
        scale = (60, 60)
        space_right = 100
        space_bottom = 100
        left = 0
        col = 1
        for player_id in players_id:
            curr_pos = (starting_sx_pos + space_right * left, starting_height + space_bottom * col)
            _render_player_id(screen, player_id, curr_pos, scale)
            left += 1
            left = left % 2
            if left == 0:
                col += 1"""
        for player_id in players_id:
            _render_player_id(screen, player_id.name, player_id.position, player_id.dimension)
    else:   
        #Schermata statica di sola attesa
        #quit_btn = pygame.Rect(80, 500, 100, 50)
        pygame.draw.rect(screen, (255, 165, 0), quit_btn)
        text = font.render("QUIT", True, (255, 255, 255))
        screen.blit(text, (quit_btn.x + 25, quit_btn.y + 10))
        scale = (100, 100)
        #position = (width/2 - scale[0]/2, height/2 - scale[1]/2)
        #plate_pos = (position[0] - 15, position[1] - 15)
        position = (width/2, height/2)
        plate_pos = (position[0], position[1])
        _render_player_id(screen, "plate", plate_pos, (scale[0] + 30, scale[1] + 30))
        _render_player_id(screen, player_id, position, scale)
        
        

def _render_player_id(screen, img_name, position, scale, render_number = False, number = None):
    full_name = img_name + ".png"
    path = Path(__file__).resolve().parent.parent / "images"/ full_name
    id = pygame.image.load(str(path)).convert_alpha()
    id = pygame.transform.scale(id, scale) 
    w, h = scale
    top_left_x = position[0] - w / 2
    top_left_y = position[1] - h / 2
    screen.blit(id, (top_left_x, top_left_y)) 
    if render_number:
        font = pygame.font.SysFont("Verdana", 48, bold=True)
        score_surface = font.render(str(number), True, (0, 0, 0)) 
        screen.blit(score_surface, (top_left_x, top_left_y))         

"""def _get_circle_positions(center, big_radius, num_circles):
    positions = []
    for i in range(num_circles):
        angle = (2 * math.pi / num_circles) * i - (math.pi / 2)
        
        x = center[0] + big_radius * math.cos(angle)
        y = center[1] + big_radius * math.sin(angle)
        
        positions.append((x, y))
    return positions"""
