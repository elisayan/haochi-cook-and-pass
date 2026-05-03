import pygame

def draw(screen, font, title_font, sub_menu, rects_dict, start_img, tutorial_img, exit_img, create_img, join_img, back_arrow_img):
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

        create = pygame.transform.smoothscale(create_img, (rects_dict["create"].width, rects_dict["create"].height))
        join = pygame.transform.smoothscale(join_img, (rects_dict["join"].width, rects_dict["join"].height))
        back_arrow = pygame.transform.smoothscale(back_arrow_img, (rects_dict["back_arrow"].width, rects_dict["back_arrow"].height))
        

        screen.blit(create, rects_dict["create"])
        screen.blit(join, rects_dict["join"])
        screen.blit(back_arrow, rects_dict["back_arrow"])
    
    