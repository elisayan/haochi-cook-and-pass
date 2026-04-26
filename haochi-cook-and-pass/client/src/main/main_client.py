import threading
import pygame
from .connection import start_network
from .model import GameModel
from .view import GameView
from .controller import GameController

if __name__ == "__main__":
    threading.Thread(target=start_network, daemon=True).start()

    pygame.init()

    pygame.display.set_caption("Haochi - Cook and Pass")

    model = GameModel()
    view = GameView()
    controller = GameController(model, view)
    
    controller.run()