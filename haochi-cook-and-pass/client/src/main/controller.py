import json
import sys
import pygame
from .connection import msg_queue, send_queue, shutdown

class GameController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        #clock = pygame.time.Clock()
        running = True
        
        while running:# and self.model.running:
            while not msg_queue.empty():
                self._handle_network(msg_queue.get())

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    print("QUIT RICEVUTO")
                    running = False
                    
                # Lo stato corrente decide cosa fare con i click/tasti
                self.model.current_state.handle_input(event, send_queue, self.model)

            #nel while loop del gioco se lo stato è PLAYING (la partita è in corso) ad ogni ciclo si deve aggiornare lo stato del gioco    
            if (self.model.current_state_key == "PLAYING"):
                self.model.current_state.update(pygame.mouse.get_pos(), self.view.screen.get_width(), self.view.screen.get_height())
            self.view.draw(self.model)
            #clock.tick(60)
        #print("running: ", running)
        #shutdown()
        #pygame.quit()
        #sys.exit()

    def _handle_network(self, raw_msg):
        data = json.loads(raw_msg)
        if data.get("action") == "ROOM_CREATED":
            self.model.game_code = data.get("code")
            self.model.set_state("LOBBY")