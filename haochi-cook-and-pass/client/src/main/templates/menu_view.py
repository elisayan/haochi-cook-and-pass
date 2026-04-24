import pygame

def draw(screen, font, sub_menu, main_btn, create_btn, join_btn):
    #screen.fill((255, 255, 255))
    
    if sub_menu == "MAIN":
        # Disegna solo il tasto START iniziale
        pygame.draw.rect(screen, (0, 200, 0), main_btn)
        text = font.render("START", True, (255, 255, 255))
        screen.blit(text, (main_btn.x + 15, main_btn.y + 10))
        
    elif sub_menu == "ROOM_CHOICE":
        # Disegna i due nuovi bottoni
        pygame.draw.rect(screen, (0, 100, 200), create_btn)
        pygame.draw.rect(screen, (200, 100, 0), join_btn)
        
        txt_create = font.render("CREATE ROOM", True, (255, 255, 255))
        txt_join = font.render("JOIN ROOM", True, (255, 255, 255))
        
        screen.blit(txt_create, (create_btn.x + 5, create_btn.y + 10))
        screen.blit(txt_join, (join_btn.x + 20, join_btn.y + 10))