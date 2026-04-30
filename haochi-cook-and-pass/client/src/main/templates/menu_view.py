import pygame

def draw(screen, font, sub_menu, rects_dict, start_img, tutorial_img, exit_img):
    #screen.fill((255, 255, 255))
    
    if sub_menu == "MAIN":
        start_rect = rects_dict["start"]
        tutorial_rect = rects_dict["tutorial"]
        exit_rect = rects_dict["exit"]

        start = pygame.transform.smoothscale(start_img, (start_rect.width, start_rect.height))
        tutorial = pygame.transform.smoothscale(tutorial_img, (tutorial_rect.width, tutorial_rect.height))
        exit_b = pygame.transform.smoothscale(exit_img, (exit_rect.width, exit_rect.height))

        # Disegna e basta
        screen.blit(start, start_rect)
        screen.blit(tutorial, tutorial_rect)
        screen.blit(exit_b, exit_rect)
        
    elif sub_menu == "ROOM_CHOICE":
        create_btn = rects_dict["create"]
        join_btn = rects_dict["join"]

        pygame.draw.rect(screen, (0, 100, 200), create_btn)
        pygame.draw.rect(screen, (200, 100, 0), join_btn)

        txt_create = font.render("CREATE ROOM", True, (255, 255, 255))
        txt_join = font.render("JOIN ROOM", True, (255, 255, 255))
        
        screen.blit(txt_create, (create_btn.x + 5, create_btn.y + 10))
        screen.blit(txt_join, (join_btn.x + 20, join_btn.y + 10))
    
    