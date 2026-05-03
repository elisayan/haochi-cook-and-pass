import pygame

def draw(screen, title_font, font, rects, back_arrow_img, input_text):
    width, height = screen.get_size()

    label = title_font.render("JOIN YOUR FRIENDS KITCHEN!", True, (255, 255, 255))
    label_rect = label.get_rect(center=(width // 2, height // 2 - 80))
    screen.blit(label, label_rect)
    
    input_rect = pygame.Rect(0, 0, 200, 50)
    input_rect.center = (width // 2, height // 2)
    pygame.draw.rect(screen, (200, 200, 200), input_rect)

    txt_surface = font.render(input_text, True, (0, 0, 0))
    txt_rect = txt_surface.get_rect(center=input_rect.center)
    screen.blit(txt_surface, txt_rect)

    instruction = font.render("Press ENTER to confirm", True, (100, 100, 100))
    instruction_rect = instruction.get_rect(center=(width // 2, height // 2 + 80))
    screen.blit(instruction, instruction_rect)

    back_arrow = pygame.transform.smoothscale(back_arrow_img, (rects["back_arrow"].width, rects["back_arrow"].height))
    screen.blit(back_arrow, rects["back_arrow"])