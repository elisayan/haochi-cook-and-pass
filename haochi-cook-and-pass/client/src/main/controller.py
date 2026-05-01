import json
import sys
import pygame
from .connection import msg_queue, send_queue, shutdown

class GameController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        clock = pygame.time.Clock()
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
                list_msg_obj = self.model.current_state.update(pygame.mouse.get_pos(), self.view.screen.get_width(), self.view.screen.get_height())
            #Il controller riceve la lista di messaggi parziali inviati dal "playing_state" e li deve completare con l'aggiunta dell'id del giocatore
                if list_msg_obj:
                    for sent_obj in list_msg_obj:
                        sent_msg = sent_obj.msg
                        sent_msg["player_id"] = self.model.player_id #TO DO il player id non serve
                        #TO DO Probabilmente non serve l'id del player perchè "controller_server", che gestisce la ricezione dei messaggi dei giocatori, conosce il giocatore che ha inviato il messaggio dato che lo riceve su una certa websocket
                        send_queue.put(json.dumps(sent_msg))    
            
            self.view.draw(self.model)
            clock.tick(60)

    def _handle_network(self, raw_msg):
        data = json.loads(raw_msg)
        if data.get("action") == "ROOM_CREATED":
            self.model.game_code = data.get("code")
            self.model.set_state("LOBBY")
            #gestito dentro a controller_server e viene inviato al target_player quando il server riceve il messaggio 
        if data.get("action") == "NEW_INGREDIENT":
            self.model.current_state.add_new_ingredient(data.get("ingr_name"), data.get("dimension"), data.get("score"), data.get("direction"))
        if data.get("action") == "STARTING_INGREDIENTS":
            #lista di tuple(nome, dimensione, score)
            self.model.current_state.add_starting_ingredients(data.get("ingredients"))       
        if data.get("action") == "STARTING_PLATES":
            #lista di tuple (nome, dimensione, score)
            self.model.current_state.add_starting_plates(data.get("plates"))     