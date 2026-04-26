import pygame

def draw(screen, font, sub_menu, create_btn, join_btn, start_img, tutorial_img, exit_img):
    #screen.fill((255, 255, 255))
    
    if sub_menu == "MAIN":
        screen_w, screen_h = screen.get_size()

        btn_w, btn_h = 220, 80

        start = pygame.transform.smoothscale(start_img, (btn_w, btn_h))
        tutorial = pygame.transform.smoothscale(tutorial_img, (btn_w, btn_h))
        exit_b = pygame.transform.smoothscale(exit_img, (btn_w, btn_h))

        center_x = screen_w // 2

        spacing = 10
        total_height = btn_h * 3 + spacing * 2
        start_y = screen_h - total_height - 20

        start_rect = start.get_rect(center=(center_x, start_y + btn_h//2))
        tutorial_rect = tutorial.get_rect(center=(center_x, start_rect.bottom + spacing + btn_h//2))
        exit_rect = exit_b.get_rect(center=(center_x, tutorial_rect.bottom + spacing + btn_h//2))

        screen.blit(start, start_rect)
        screen.blit(tutorial, tutorial_rect)
        screen.blit(exit_b, exit_rect)

        return {
            "start": start_rect,
            "tutorial": tutorial_rect,
            "exit": exit_rect
        }
        
    elif sub_menu == "ROOM_CHOICE":
        # Disegna i due nuovi bottoni
        pygame.draw.rect(screen, (0, 100, 200), create_btn)
        pygame.draw.rect(screen, (200, 100, 0), join_btn)
        
        txt_create = font.render("CREATE ROOM", True, (255, 255, 255))
        txt_join = font.render("JOIN ROOM", True, (255, 255, 255))
        
        screen.blit(txt_create, (create_btn.x + 5, create_btn.y + 10))
        screen.blit(txt_join, (join_btn.x + 20, join_btn.y + 10))

        return {
            "create": create_btn,
            "join": join_btn
        }
    
    