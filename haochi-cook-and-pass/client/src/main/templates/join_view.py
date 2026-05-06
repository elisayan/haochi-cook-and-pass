import pygame

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