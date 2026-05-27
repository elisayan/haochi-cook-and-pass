import pygame

def draw(screen, title_font, font, small_font, rects, scores):
    screen.fill((245, 235, 225))
    cx = screen.get_width() // 2
    cy = screen.get_height() // 2

    card_width = 400
    card_x = cx - card_width // 2

    you_rows = [("Dishes", scores["player"]["dishes"]), ("Points", scores["player"]["points"])]
    team_rows = [("Dishes", scores["team"]["dishes"]), ("Points", scores["team"]["points"])]

    # Titolo fisso in alto
    main_title = title_font.render("SCOREBOARD", True, (180, 100, 30))
    screen.blit(main_title, main_title.get_rect(centerx=cx, top=20))
    sub = small_font.render("Game complete!", True, (200, 140, 80))
    screen.blit(sub, sub.get_rect(centerx=cx, top=20 + main_title.get_height() + 4))

    # Calcola altezza totale delle card + bottone per centrare verticalmente
    card_h = lambda rows: 60 + len(rows) * 36
    gap = 16
    btn_h = 48
    btn_gap = 36
    total_h = card_h(you_rows) + gap + card_h(team_rows) + btn_gap + btn_h
    start_y = cy - total_h // 2 + 40

    def draw_card(y, label, icon_color, rows):
        card = pygame.Rect(card_x, y, card_width, 60 + len(rows) * 36)
        pygame.draw.rect(screen, (255, 250, 244), card, border_radius=14)
        pygame.draw.rect(screen, (255, 180, 100), card, 2, border_radius=14)

        pygame.draw.circle(screen, icon_color, (card_x + 28, y + 24), 16)

        header = small_font.render(label.upper(), True, (150, 100, 40))
        screen.blit(header, (card_x + 52, y + 16))

        pygame.draw.line(screen, (255, 200, 140),
                         (card_x + 12, y + 46), (card_x + card_width - 12, y + 46), 1)

        for i, (lbl, val) in enumerate(rows):
            row_y = y + 56 + i * 36
            text_lbl = font.render(lbl, True, (130, 100, 60))
            text_val = font.render(str(val), True, (180, 100, 30))
            screen.blit(text_lbl, (card_x + 16, row_y))
            screen.blit(text_val, (card_x + card_width - text_val.get_width() - 16, row_y))
            if i < len(rows) - 1:
                pygame.draw.line(screen, (240, 220, 200),
                                 (card_x + 12, row_y + 30), (card_x + card_width - 12, row_y + 30), 1)
        return card

    you_card = draw_card(start_y, "You", (255, 180, 100), you_rows)
    team_card = draw_card(you_card.bottom + gap, "Team", (255, 160, 60), team_rows)

    # Bottone fisso in basso
    home_btn = pygame.Rect(0, 0, 200, btn_h)
    home_btn.center = (cx, screen.get_height() - 70)
    pygame.draw.rect(screen, (255, 160, 60), home_btn, border_radius=24)
    home_text = font.render("HOME", True, (255, 255, 255))
    screen.blit(home_text, home_text.get_rect(center=home_btn.center))
    rects["home_btn"] = home_btn