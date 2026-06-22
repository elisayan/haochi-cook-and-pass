import threading
import pygame
import sys
from .connection import start_network
from .model import GameModel
from .view import GameView
from .controller import GameController

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_ip = sys.argv[1]
    else:
        target_ip = "localhost" 
        print(f"Nessun IP specificato da linea di comando. Si usa il server locale: {target_ip}")

    threading.Thread(target=start_network, args=(target_ip,), daemon=True).start()
    #threading.Thread(target=start_network, daemon=True).start()

    pygame.init()

    pygame.display.set_caption("Haochi - Cook and Pass")

    model = GameModel()
    view = GameView()
    controller = GameController(model, view)
    
    controller.run()