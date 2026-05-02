import pygame
import math
import json
from .base_state import BaseState
from ..utilities import *

#Per rimuovere il testing mettere is_starting_player a False e commentare riga 23 e nella "view" togliere il room_code fittizio riga 20 e commentare riga 16

class LobbyState(BaseState):
    def __init__(self, model):
        super().__init__(model)
        #todo aggiungere lista dei giocatori e il loro stato di ready
        #self.players_ready = ["orange", "pepper", "rice", "shrimp"]
        self.ready_players = [] #lista di Player_Id 
        self.is_starting_player = True
        self.room_code = model.game_code
        self.plates = [] #lista di Element che rappresentano i piatti
        self.circle = ((500, 260), 200) #cerchio su cui si trovano i piatti (center, radius)
        self.playing_turn = {} #giro della partita #piatto e player_id
        self.quit_btn = pygame.Rect(80, 500, 100, 50)
        self.start_btn = pygame.Rect(620, 500, 100, 50)
        #TO DO da rimuovere perchè usato solo per testing
        self.update_players_in_game(["orange", "pepper", "rice", "shrimp"], self.is_starting_player) #TO DO da rimuovere, usato solo per fare delle prove
        

    def handle_input(self, event, send_queue, model):
        #TO DO Con la send_queue si può mandare al server direttamente il messaggio di start e stop
# Inoltre si ha anche il model allora anche l'ordine del giro si potrebbe mandare direttamente qui 
        if event.type == pygame.QUIT:# TO DO mandare messaggio che il giocatore lascia la partita 
            send_queue.put(json.dumps({"action": "QUIT_ROOM"}))     
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_btn.collidepoint(event.pos):
                #Quando viene cliccato si verifica che tutti gli id siano stati sistemati
                print(len(self.ready_players))
                print(len(self.playing_turn))
                if len(self.playing_turn) == len(self.ready_players) and len(self.playing_turn) >= 2:
                    print("Si invia messaggio al server")
                    order_players = []
                    for i in range(max(self.playing_turn), -1, -1):
                        order_players.append(self.playing_turn[i].name)
                    print(order_players)
                    send_queue.put(json.dumps({
                        "action": "START_PLAYING",
                        "players_position": order_players
                    }))    
            if self.quit_btn.collidepoint(event.pos):       
                print("Si deve dire al server che il giocatore vuole uscire dalla partita")
                send_queue.put(json.dumps({"action": "QUIT_ROOM"})) 
            self.handle_pression(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_release()

#Metodo chiamato dal controller per aggiornare la posizione degli elementi nella finestra di gioco del giocatore iniziale
    def update(self, mouse_pos, screen_width, screen_height):
        for player_id in self.ready_players:
            player_id.update_position(mouse_pos, screen_width, screen_height)

#funzione invocata quando il giocatore riceve dal server un messaggio "PLAYERS_IN_GAME"
#usata per aggiornare l'id dei giocatori presenti nella partita e sapere se il giocatore che ha ricevuto
#il messaggio è quello che ha iniziato la partita
    def update_players_in_game(self, players_id, is_starting_player):
        print(players_id)
        #Si resettano i piatti e gli id dei giocatori
        self._update_turn_game(players_id)
        self.ready_players = []
        self.plates = []
        #self.ready_players = players_id #non sono più lista di id (stringhe nomi ingredienti) ma oggetti Player_Id
        scale = (60, 60)
        #Definizione della posizione di ogni id dei giocatori in attesa
        starting_sx_pos = 80
        starting_height_pos = 70
        space_right = 100
        space_bottom = 100
        left = 0
        col = 1
        for player_id in players_id:
            curr_pos = (starting_sx_pos + space_right * left, starting_height_pos + space_bottom * col)
            player_id_obj = Player_Id(player_id + ".png", scale, curr_pos) 
            left += 1
            left = left % 2
            if left == 0:
                col += 1
            self.ready_players.append(player_id_obj)    

        self.is_starting_player = is_starting_player
        self._update_plates()

    def _update_turn_game(self, players_id):
        previous_players_id = []
        for player in self.ready_players:
            previous_players_id.append(player.name)
        #giocatori rimossi
        removed_players = list(set(previous_players_id) - set(players_id))
        print(removed_players)
        for removed_player in removed_players:
            is_present_play_turn = False
            index_plate = None
            for key, value in self.playing_turn.items():
                if value.name == removed_player:
                    index_plate = key
                    is_present_play_turn = True
                    break
            if is_present_play_turn:
                print(index_plate)
                succ = index_plate + 1
                #si spostano indietro ai piatti precedenti gli id dei giocatori già collocati
                self._shift_players_backward(succ, max(self.playing_turn) + 1)
            
            if not self.playing_turn:
                return
            #si trova il piatto libero e si sostituisce con l'id del giocatore presente dopo
            for i in range(0, max(self.playing_turn)):
                if self.playing_turn.get(i) is None:
                    self._shift_players_backward(i + 1, max(self.playing_turn) + 1)
    def _shift_players_backward(self, inf, sup):
        for i in range(inf, sup):
                    if self.playing_turn.get(i):
                        self.playing_turn[i - 1] = self.playing_turn.get(i)
                        del self.playing_turn[i]
                        print("L'id", self.playing_turn[i - 1].name, "è stato spostato ad indice del piatto", i - 1)


    def _update_plates(self):
        plates_pos = self._get_plates_positions(self.circle[0], self.circle[1], len(self.ready_players))
        plate_scale = 100
        for index, pos in enumerate(plates_pos):
            plate = Element("plate.png", (plate_scale, plate_scale), pos)#(pos[0] - plate_scale/2, pos[1] - plate_scale/2)
            plate.set_plate()
            self.plates.append(plate)
            if self.playing_turn.get(index):
                player_id = self.playing_turn.get(index)
                #Aggiornamento della posizione nel piatto
                for player in self.ready_players:
                    if player.name == player_id.name:
                        player.position = pos
                        player.is_in_plate = True

    def _get_plates_positions(self, center, big_radius, num_circles):
        positions = []
        for i in range(num_circles):
            angle = (2 * math.pi / num_circles) * i - (math.pi / 2)
            
            x = center[0] + big_radius * math.cos(angle)
            y = center[1] + big_radius * math.sin(angle)
            
            positions.append((x, y))
        return positions           

    def handle_pression(self, mouse_pos):
        for elem in self.ready_players:
            #aggiorna il dragging a True per l'id dell'utente
            elem.check_click(mouse_pos)

    def handle_release(self):
    #Verifica se ci sono oggetti fuori dai piatti e che non sono nella loro posizione originale    
        for elem in self.ready_players:
            #aggiorna il dragging a True per l'id dell'utente
            elem.stop_dragging()
            if not elem.is_in_plate:
                #se l'ingrediente si trova all'interno del piatto nel momento in cui è rilasciato allora lo si deve lasciare lì
                found_collision = False
                for index, plate in enumerate(self.plates):
                    if elem.detect_collision_plate(plate):
                        found_collision = True
                        #Verificare che non ci siano già altri player_id nel piatto, altrimenti riportare quello rilasciato nella sua posizione originale
                        """is_already_occupied = False
                        for pid in self.ready_players:
                            if pid != elem and pid.is_in_plate and np.allclose(pid.position, plate.position): #numpy array identici
                                is_already_occupied = True
                                break"""
                        #if not is_already_occupied:
                        if self.playing_turn.get(index) is not None:
                            #si cerca di mettere l'id dell'utente in un piatto già occupato
                            #si sostituiscono i due elementi
                            previous_elem = self.playing_turn[index]
                            previous_elem.position = previous_elem.original_pos 
                            previous_elem.is_in_plate = False 
                        elem.is_in_plate = True
                        elem.position = plate.position
                        elem.velocity = np.zeros(2)
                        #aggiornamento del dizionario
                        self.playing_turn[index] = elem
                        break
                if not found_collision:#si è lasciato l'id dell'utente svolazzante
                    elem.position = elem.original_pos 
            else:#si verifica se l'id del giocatore è ancora dentro a un piatto
                is_still_in_plate = False
                for plate in self.plates:
                    if np.allclose(elem.position, plate.position):
                        is_still_in_plate = True
                        break
                if not is_still_in_plate:
                    elem.position = elem.original_pos 
                    elem.is_in_plate = False
                    elem.velocity = np.zeros(2)
                    for key, value in self.playing_turn.items():
                        if value == elem:
                            self.playing_turn[key] = None
                            break                   
                                
                        