class BaseState:
    def __init__(self, game):
        self.game = game #cambio di stato

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass