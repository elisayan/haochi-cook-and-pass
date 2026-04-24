import json
import pygame
from .connection import msg_queue, send_queue

class GameController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            while not msg_queue.empty():
                self._handle_network(msg_queue.get())

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                # Lo stato corrente decide cosa fare con i click/tasti
                self.model.current_state.handle_input(event, send_queue, self.model)

            self.view.draw(self.model)
            clock.tick(60)

    def _handle_network(self, raw_msg):
        data = json.loads(raw_msg)
        if data.get("action") == "ROOM_CREATED":
            self.model.game_code = data.get("code")
            self.model.set_state("LOBBY")