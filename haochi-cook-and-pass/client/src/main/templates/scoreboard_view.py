import pygame
from pathlib import Path

def draw(screen, title_font, font, rects, back_arrow_img, scores):
    #screen.fill((245, 235, 225))

    cx = screen.get_width() // 2  # centro orizzontale

    main_title = title_font.render("SCOREBOARD", True, (180, 100, 30))
    title_rect = main_title.get_rect(centerx=cx, top=20)
    screen.blit(main_title, title_rect)

    score_card = pygame.Rect(0, 0, 400, 300)
    score_card.centerx = cx
    score_card.top = 120
    pygame.draw.rect(screen, (255, 248, 240), score_card, border_radius=12)
    pygame.draw.rect(screen, (255, 180, 100), score_card, 2, border_radius=12)

    label = font.render("FINAL SCORES:", True, (150, 130, 110))
    screen.blit(label, (score_card.x + 15, score_card.y + 15))

    for i, (player_name, player_score) in enumerate(scores.items()):
        score_text = font.render(f"{player_name}: {player_score} points", True, (100, 100, 200))
        screen.blit(score_text, (score_card.x + 15, score_card.y + 50 + i * 30))

    home_btn = pygame.Rect(0, 0, 160, 45)
    home_btn.center = (cx, score_card.bottom + 40)
    pygame.draw.rect(screen, (255, 160, 60), home_btn, border_radius=22)
    home_text = font.render("HOME", True, (255, 255, 255))
    screen.blit(home_text, home_text.get_rect(center=home_btn.center))

    rects["home_btn"] = home_btn