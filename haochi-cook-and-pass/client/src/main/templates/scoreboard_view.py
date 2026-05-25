import pygame

def draw(screen, title_font, font, rects, back_arrow_img, scores):
    screen.fill((245, 235, 225))

    cx = screen.get_width() // 2

    main_title = title_font.render("SCOREBOARD", True, (180, 100, 30))
    screen.blit(main_title, main_title.get_rect(centerx=cx, top=20))

    card_width = 400
    card_x = cx - card_width // 2

    #Card YOU
    you_rows = [
        ("Dishes", scores["player"]["dishes"]),
        ("Points", scores["player"]["points"]),
        #("Level",  scores["player"]["level"])
    ]
    you_card = pygame.Rect(card_x, 100, card_width, 50 + len(you_rows) * 30)
    pygame.draw.rect(screen, (255, 248, 240), you_card, border_radius=12)
    pygame.draw.rect(screen, (255, 180, 100), you_card, 2, border_radius=12)

    you_label = font.render(f"YOU ", True, (150, 130, 110))
    screen.blit(you_label, (you_card.x + 15, you_card.y + 12))

    for i, (label, value) in enumerate(you_rows):
        text = font.render(f"{label}: {value}", True, (100, 100, 200))
        screen.blit(text, (you_card.x + 15, you_card.y + 40 + i * 30))

    #Card TEAM
    team_rows = [
        ("Dishes", scores["team"]["dishes"]),
        ("Points", scores["team"]["points"])
    ]
    team_card = pygame.Rect(card_x, you_card.bottom + 20, card_width, 50 + len(team_rows) * 30)
    pygame.draw.rect(screen, (255, 248, 240), team_card, border_radius=12)
    pygame.draw.rect(screen, (255, 180, 100), team_card, 2, border_radius=12)

    team_label = font.render("TEAM", True, (150, 130, 110))
    screen.blit(team_label, (team_card.x + 15, team_card.y + 12))

    for i, (label, value) in enumerate(team_rows):
        text = font.render(f"{label}: {value}", True, (100, 100, 200))
        screen.blit(text, (team_card.x + 15, team_card.y + 40 + i * 30))

    home_btn = pygame.Rect(0, 0, 160, 45)
    home_btn.center = (cx, team_card.bottom + 40)
    pygame.draw.rect(screen, (255, 160, 60), home_btn, border_radius=22)
    home_text = font.render("HOME", True, (255, 255, 255))
    screen.blit(home_text, home_text.get_rect(center=home_btn.center))

    rects["home_btn"] = home_btn