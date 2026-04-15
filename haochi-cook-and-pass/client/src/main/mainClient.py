from view.view import GameView
from model import Client
from controller.controller import GameController

"""Il Client è implementato in __init__.py"""

if __name__ == "__main__":
    # La View si inizializza e chiama pygame.init() internamente
    view = GameView()
    model = Client()
    
    # Il controller agisce da coordinatore tra i due
    app = GameController(model, view)
    app.run()