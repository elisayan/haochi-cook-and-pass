import pygame

def draw(screen, font, input_text):
    screen.fill((255, 255, 255))
    label = font.render("Join your friends kitchen:", True, (0, 0, 0))
    screen.blit(label, (250, 200))
    
    # Rettangolo per il testo inserito
    input_rect = pygame.Rect(300, 250, 200, 50)
    pygame.draw.rect(screen, (200, 200, 200), input_rect)
    
    txt_surface = font.render(input_text, True, (0, 0, 0))
    screen.blit(txt_surface, (input_rect.x + 5, input_rect.y + 10))
    
    instruction = font.render("Press ENTER to confirm", True, (100, 100, 100))
    screen.blit(instruction, (260, 320))