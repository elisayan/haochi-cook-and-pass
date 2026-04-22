import pygame

def draw(screen, button_rect, font):
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 200, 0), button_rect)
    btn_text = font.render("START", True, (255, 255, 255))
    screen.blit(btn_text, (button_rect.x + 15, button_rect.y + 10))