"""pagina di attesa di un segnale Start dal server"""
import pygame

def draw(screen, game_code, font, code_font):
    screen.fill((255, 255, 255))
    label = font.render("Codice Stanza:", True, (0, 0, 0))
    code_text = code_font.render(game_code, True, (0, 0, 255))
    screen.blit(label, (340, 150))
    screen.blit(code_text, (355, 180))