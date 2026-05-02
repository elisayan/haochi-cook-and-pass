import pygame

def draw(screen, font, title_font, sub_menu, rects_dict, start_img, tutorial_img, exit_img):
    #screen.fill((255, 255, 255))
    
    if sub_menu == "MAIN":
        start = pygame.transform.smoothscale(start_img, (rects_dict["start"].width, rects_dict["start"].height))
        tutorial = pygame.transform.smoothscale(tutorial_img, (rects_dict["tutorial"].width, rects_dict["tutorial"].height))
        exit_b = pygame.transform.smoothscale(exit_img, (rects_dict["exit"].width, rects_dict["exit"].height))

        screen.blit(start, rects_dict["start"])
        screen.blit(tutorial, rects_dict["tutorial"])
        screen.blit(exit_b, rects_dict["exit"])

    elif sub_menu == "ROOM_CHOICE":
        color = (255, 255, 255) # Bianco
        line1 = title_font.render("JOIN A FRIEND'S KITCHEN", True, color)
        line2 = title_font.render("OR", True, color)
        line3 = title_font.render("CREATE A NEW ONE YOURSELF", True, color)

        center_x = screen.get_width() // 2

        screen.blit(line1, (center_x - line1.get_width() // 2, 100))
        screen.blit(line2, (center_x - line2.get_width() // 2, 155))
        screen.blit(line3, (center_x - line3.get_width() // 2, 205))

        create_btn = rects_dict["create"]
        join_btn = rects_dict["join"]

        pygame.draw.rect(screen, (0, 100, 200), create_btn)
        pygame.draw.rect(screen, (200, 100, 0), join_btn)

        txt_create = font.render("CREATE ROOM", True, (255, 255, 255))
        txt_join = font.render("JOIN ROOM", True, (255, 255, 255))
        
        screen.blit(txt_create, (create_btn.centerx - txt_create.get_width() // 2, create_btn.centery - txt_create.get_height() // 2))
        screen.blit(txt_join, (join_btn.centerx - txt_join.get_width() // 2, join_btn.centery - txt_join.get_height() // 2))
    
    