import pygame
import math
from pathlib import Path

def draw(screen, title_font, font, rects, back_arrow_img, input_text, error_message):
    width, height = screen.get_size()
    
    card_width, card_height = 500, 400  # Aumentata l'altezza per l'errore
    card_rect = pygame.Rect(0, 0, card_width, card_height)
    card_rect.center = (width // 2, height // 2)
    
    shadow_rect = card_rect.copy()
    shadow_rect.y += 5
    pygame.draw.rect(screen, (255, 248, 240), card_rect, border_radius=20)
    pygame.draw.rect(screen, (255, 180, 100), card_rect, 3, border_radius=20)
    
    title = title_font.render("JOIN A KITCHEN", True, (180, 100, 50))
    title_rect = title.get_rect(center=(width // 2, card_rect.top + 60))
    screen.blit(title, title_rect)
    
    subtitle = font.render("Enter the room code below", True, (150, 130, 110))
    subtitle_rect = subtitle.get_rect(center=(width // 2, card_rect.top + 100))
    screen.blit(subtitle, subtitle_rect)
    
    input_rect = pygame.Rect(0, 0, 280, 55)
    input_rect.center = (width // 2, card_rect.centery - 20)  # Leggermente più in alto
    
    glow_rect = input_rect.inflate(8, 8)
    pygame.draw.rect(screen, (255, 200, 150, 100), glow_rect, border_radius=15)
    pygame.draw.rect(screen, (255, 255, 255), input_rect, border_radius=12)
    
    # Cambia il bordo in rosso se c'è un errore
    border_color = (255, 80, 80) if error_message else (255, 160, 80)
    pygame.draw.rect(screen, border_color, input_rect, 2, border_radius=12)
    
    if input_text:
        txt_surface = font.render(input_text, True, (60, 40, 30))
    else:
        txt_surface = font.render("Room Code...", True, (180, 160, 140))
    txt_rect = txt_surface.get_rect(center=input_rect.center)
    screen.blit(txt_surface, txt_rect)
    
    if pygame.time.get_ticks() % 1000 < 500:
        cursor_x = txt_rect.right + 2 if input_text else input_rect.centerx
        cursor_y = input_rect.centery - 12
        pygame.draw.line(screen, (255, 160, 80), 
                        (cursor_x, cursor_y), 
                        (cursor_x, cursor_y + 24), 2)
    
    if error_message:
        error_bg_rect = pygame.Rect(0, 0, card_width - 60, 50)
        error_bg_rect.center = (width // 2, card_rect.centery + 50)
        error_surface = pygame.Surface((error_bg_rect.width, error_bg_rect.height), pygame.SRCALPHA)
        corner_radius = 12
        pygame.draw.rect(error_surface, (255, 200, 200, 200), 
                        error_surface.get_rect(), 
                        border_radius=corner_radius)
        #error_surface.fill((255, 200, 200, 180))
        screen.blit(error_surface, error_bg_rect)
        
        error_text = font.render(error_message, True, (200, 40, 40))
        error_text_rect = error_text.get_rect(center=error_bg_rect.center)
        screen.blit(error_text, error_text_rect)
    
    btn_width, btn_height = 150, 45
    btn_rect = pygame.Rect(0, 0, btn_width, btn_height)
    btn_rect.center = (width // 2, card_rect.bottom - 50)
    
    btn_color = (255, 160, 60) if input_text else (200, 200, 190)
    pygame.draw.rect(screen, btn_color, btn_rect, border_radius=22)
    
    btn_text = font.render("JOIN", True, (255, 255, 255))
    btn_text_rect = btn_text.get_rect(center=btn_rect.center)
    screen.blit(btn_text, btn_text_rect)
    
    back_arrow = pygame.transform.smoothscale(back_arrow_img, 
                                             (rects["back_arrow"].width, 
                                              rects["back_arrow"].height))
    screen.blit(back_arrow, rects["back_arrow"])

def draw_await_join(screen, title_font, font, rects, ingr_id, back_arrow_img, error_message):
    #screen.fill((245, 235, 225)) 

    parent = Path(__file__).resolve().parent.parent / "images" / "ingredients"
    img_path = parent / f"{ingr_id}.png"
    if not img_path.exists():
        img_path = parent / f"{ingr_id}.PNG"

    width, height = screen.get_size()
    ticks = pygame.time.get_ticks()

    title_line1 = title_font.render("SHOW YOUR INGREDIENT", True, (180, 100, 50))
    title_line2 = title_font.render("TO THE HEAD CHEF!", True, (180, 100, 50))
    
    line_spacing = 5
    #title_height = title_line1.get_height() + title_line2.get_height() + line_spacing
    title_y = height // 6
    
    title1_rect = title_line1.get_rect(center=(width // 2, title_y))
    title2_rect = title_line2.get_rect(center=(width // 2, title_y + title_line1.get_height() + line_spacing))
    
    screen.blit(title_line1, title1_rect)
    screen.blit(title_line2, title2_rect)

    back_arrow = pygame.transform.smoothscale(back_arrow_img, 
                                             (rects["back_arrow"].width, 
                                              rects["back_arrow"].height))
    screen.blit(back_arrow, rects["back_arrow"])

    try:
        ingredient_img = pygame.image.load(str(img_path)).convert_alpha()
        ingredient_img = pygame.transform.smoothscale(ingredient_img, (120, 120))
        
        offset_y = math.sin(ticks * 0.005) * 10 
        img_rect = ingredient_img.get_rect(center=(width // 2, (height // 2) + offset_y))
        
        aura_surface = pygame.Surface((180, 180), pygame.SRCALPHA)
        pygame.draw.circle(aura_surface, (255, 220, 180, 100), (90, 90), 90)
        screen.blit(aura_surface, (img_rect.centerx - 90, img_rect.centery - 90))
        screen.blit(ingredient_img, img_rect)
        
        name_surf = font.render(ingr_id.upper(), True, (100, 70, 50))
        name_rect = name_surf.get_rect(center=(width // 2, img_rect.bottom + 30))
        screen.blit(name_surf, name_rect)
        
        dots = "." * ((ticks // 500) % 4)
        waiting_text = font.render(f"Waiting for the head chef{dots}", True, (150, 130, 110))
        waiting_rect = waiting_text.get_rect(center=(width // 2, height - 120))
        screen.blit(waiting_text, waiting_rect)
        
    except pygame.error:
        print(f"Errore: Impossibile trovare l'immagine {img_path}")
        error_text = font.render(f"Ingredient image not found: {ingr_id}", True, (200, 40, 40))
        error_rect = error_text.get_rect(center=(width // 2, height // 2))
        screen.blit(error_text, error_rect)

    if error_message:
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        # Dimensioni del popup
        popup_width = 400
        popup_height = 200
        popup_rect = pygame.Rect(0, 0, popup_width, popup_height)
        popup_rect.center = (width // 2, height // 2)
        
        # Sfondo del popup
        pygame.draw.rect(screen, (255, 248, 240), popup_rect, border_radius=20)
        pygame.draw.rect(screen, (255, 180, 100), popup_rect, 3, border_radius=20)
        
        # Icona di errore (X rossa)
        icon_center = (popup_rect.centerx, popup_rect.top + 45)
        pygame.draw.circle(screen, (200, 60, 60), icon_center, 25)
        error_icon = font.render("!", True, (255, 255, 255))
        error_icon_rect = error_icon.get_rect(center=icon_center)
        screen.blit(error_icon, error_icon_rect)
        
        # Testo di errore
        error_title = font.render("ERROR", True, (200, 60, 60))
        error_title_rect = error_title.get_rect(center=(popup_rect.centerx, popup_rect.top + 85))
        screen.blit(error_title, error_title_rect)
        
        error_msg_text = font.render(error_message, True, (100, 70, 50))
        error_msg_rect = error_msg_text.get_rect(center=(popup_rect.centerx, popup_rect.top + 120))
        screen.blit(error_msg_text, error_msg_rect)
        
        # Pulsante per tornare alla home
        home_btn = pygame.Rect(0, 0, 160, 45)
        home_btn.center = (popup_rect.centerx, popup_rect.bottom - 50)
        pygame.draw.rect(screen, (255, 160, 60), home_btn, border_radius=22)
        home_text = font.render("GO TO HOME", True, (255, 255, 255))
        home_text_rect = home_text.get_rect(center=home_btn.center)
        screen.blit(home_text, home_text_rect)
        
        # Salva il rettangolo del pulsante per gestire il click nello stato
        rects["error_home_btn"] = home_btn