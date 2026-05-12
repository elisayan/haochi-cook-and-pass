import pygame
import math
from pathlib import Path

C_BG = (255, 248, 240)      # Sfondo card/riquadri
C_BORDER = (255, 180, 100)  # Arancio bordi
C_TITLE = (180, 100, 30)    # Marrone titoli
C_SUBTITLE = (150, 130, 110)# Grigio/Marrone testi secondari

def draw(screen, game_code, player_id, players_id, is_starting_player, font, title_font, code_font, circle, plates, start_btn, quit_btn):
    screen.fill((245, 235, 225)) 
    
    width, height = screen.get_size()

    main_title = title_font.render("KITCHEN CREATED", True, C_TITLE)
    title_rect = main_title.get_rect(topleft=(40, 20))
    screen.blit(main_title, title_rect)
    
    code_card = pygame.Rect(40, 120, 180, 80)
    pygame.draw.rect(screen, C_BG, code_card, border_radius=12)
    pygame.draw.rect(screen, C_BORDER, code_card, 2, border_radius=12)
    
    label = font.render("CODE:", True, C_SUBTITLE)
    code_text = code_font.render(game_code, True, (100, 100, 200)) 
    screen.blit(label, (code_card.x + 15, code_card.y + 5))
    screen.blit(code_text, (code_card.x + 15, code_card.y + 30))

    player_list_card = pygame.Rect(40, 220, 360, 180)
    pygame.draw.rect(screen, C_BG, player_list_card, border_radius=15)
    pygame.draw.rect(screen, C_BORDER, player_list_card, 2, border_radius=15)

    player_label = font.render("CHEFS LIST:", True, C_SUBTITLE)
    screen.blit(player_label, (player_list_card.x + 15, player_list_card.y + 5))

    suggestion_label = font.render("Share your kitchen code with other chefs!", True, C_SUBTITLE)
    screen.blit(suggestion_label, (40, 80))

    if is_starting_player:
        center = circle[0]
        radius = circle[1]
        #right_margin = 80
        #center_x = width - radius - right_margin
        #center_y = height // 2
        #center = (center_x, center_y)

        pygame.draw.circle(screen, (255, 255, 255), center, radius)
        draw_dashed_circle(screen, C_BORDER, center, radius, width=3, dash_length=8)
        
        # Rendering Piatti e Giocatori
        for i, plate in enumerate(plates):
            _render_player_id(screen, "plate", plate.position, plate.dimension, render_number=True, number=i)
        
        for player in players_id:
            _render_player_id(screen, player.name, player.position, player.dimension)
            
        is_ready = len(players_id) >= 2 and len(plates) > 0 # o altra logica simile
    
        # Colore: Verde se pronto, Grigio se disabilitato
        start_color = (100, 200, 100) if is_ready else (180, 180, 180)
    
        pygame.draw.rect(screen, start_color, start_btn, border_radius=20)
        btn_txt = font.render("START", True, (255, 255, 255))
        screen.blit(btn_txt, btn_txt.get_rect(center=start_btn.center))
        
    #else:   
        #Schermata statica di sola attesa
        #quit_btn = pygame.Rect(80, 500, 100, 50)
        #pygame.draw.rect(screen, (255, 165, 0), quit_btn)
        #text = font.render("QUIT", True, (255, 255, 255))
        #screen.blit(text, (quit_btn.x + 25, quit_btn.y + 10))
        #scale = (100, 100)
        #position = (width/2 - scale[0]/2, height/2 - scale[1]/2)
        #plate_pos = (position[0] - 15, position[1] - 15)
        #position = (width/2, height/2)
        #plate_pos = (position[0], position[1])
        #_render_player_id(screen, "plate", plate_pos, (scale[0] + 30, scale[1] + 30))
        #_render_player_id(screen, player_id, position, scale)

    #quit_rect = pygame.Rect(40, height - 80, 120, 50)
    pygame.draw.rect(screen, (255, 120, 100), quit_btn, border_radius=20)
    quit_txt = font.render("EXIT", True, (255, 255, 255))
    screen.blit(quit_txt, quit_txt.get_rect(center=quit_btn.center))

def draw_dashed_circle(surface, color, center, radius, width=2, dash_length=10):
    """Disegna un cerchio tratteggiato calcolando i punti sulla circonferenza."""
    import math
    circumference = 2 * math.pi * radius
    num_dashes = int(circumference / (dash_length * 2))
    
    for i in range(num_dashes):
        # Angolo di inizio e fine per ogni tratto (in radianti)
        start_angle = (i * 2 * math.pi / num_dashes)
        end_angle = start_angle + (dash_length / radius)
        
        # Disegniamo un arco per ogni tratto
        pygame.draw.arc(surface, color, 
                        (center[0]-radius, center[1]-radius, radius*2, radius*2), 
                        start_angle, end_angle, width)

def _render_player_id(screen, img_name, position, scale, render_number=False, number=None):
    # Correzione estensione per evitare duplicati .PNG.PNG
    clean_name = img_name.replace(".PNG", "").replace(".png", "")
    full_name = f"{clean_name}.PNG"
    
    path = Path(__file__).resolve().parent.parent / "images" / "ingredients" / full_name
    
    try:
        img = pygame.image.load(str(path)).convert_alpha()
        img = pygame.transform.smoothscale(img, scale)
        rect = img.get_rect(center=position)
        screen.blit(img, rect)
        
        if render_number:
            num_font = pygame.font.SysFont("Verdana", 24, bold=True)
            # Piccolo cerchio per il numero del piatto
            pygame.draw.circle(screen, (255, 255, 255), (rect.centerx, rect.top), 15)
            pygame.draw.circle(screen, C_BORDER, (rect.centerx, rect.top), 15, 2)
            num_surf = num_font.render(str(number), True, (60, 40, 30))
            screen.blit(num_surf, num_surf.get_rect(center=(rect.centerx, rect.top)))
    except:
        pass # Gestione errore silenziosa per brevità