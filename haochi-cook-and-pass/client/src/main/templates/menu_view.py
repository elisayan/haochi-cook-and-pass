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
        color = (255, 255, 255)
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

    elif sub_menu == "TUTORIAL":
        width, height = screen.get_size()
        
        card_width, card_height = 700, 500
        card_rect = pygame.Rect(0, 0, card_width, card_height)
        card_rect.center = (width // 2, height // 2)
        
        pygame.draw.rect(screen, (255, 248, 240), card_rect, border_radius=20)
        pygame.draw.rect(screen, (255, 180, 100), card_rect, 3, border_radius=20)
        
        title = title_font.render("HOW TO PLAY", True, (180, 100, 50))
        title_rect = title.get_rect(center=(width // 2, card_rect.top + 50))
        screen.blit(title, title_rect)
        
        line_rect = pygame.Rect(0, 0, 300, 2)
        line_rect.center = (width // 2, card_rect.top + 85)
        pygame.draw.rect(screen, (255, 180, 100), line_rect)
        
        instructions = [
            "Each player is identified with an ingredient",
            "The HEAD CHEF will decide the order of your placement",
            "Once they're ready, the HEAD CHEF starts the game",
            "Pass the ingredients they need to your friends",
            "Follow the recipe sequence to cook the perfect dish!"
        ]
        
        y_offset = card_rect.top + 120
        for i, instruction in enumerate(instructions):
            bullet = font.render("•", True, (255, 160, 60))
            bullet_rect = bullet.get_rect(topleft=(card_rect.left + 50, y_offset + i * 35))
            screen.blit(bullet, bullet_rect)
            
            text = font.render(instruction, True, (100, 70, 50))
            text_rect = text.get_rect(topleft=(bullet_rect.right + 10, y_offset + i * 35))
            screen.blit(text, text_rect)
        
        tip_title = font.render("TIP:", True, (255, 160, 60))
        tip_title_rect = tip_title.get_rect(topleft=(card_rect.left + 50, card_rect.bottom - 100))
        screen.blit(tip_title, tip_title_rect)
        
        tip_text = font.render("Communicate with your team to win!", True, (150, 130, 110))
        tip_text_rect = tip_text.get_rect(topleft=(tip_title_rect.right + 10, card_rect.bottom - 100))
        screen.blit(tip_text, tip_text_rect)
        
        back_arrow = pygame.transform.smoothscale(back_arrow_img, (rects_dict["back_arrow"].width, rects_dict["back_arrow"].height))
        screen.blit(back_arrow, rects_dict["back_arrow"])
    