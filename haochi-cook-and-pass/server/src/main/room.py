DIFFICULTY_ORDER = ["easy", "medium", "hard"]

class RoomState:
    INIT = "INIT"
    READY = "READY"
    IN_GAME = "IN_GAME"
    OVER = "OVER"


class Room:
    def __init__(self, room_code):
        self.code = room_code
        self.state = RoomState.INIT
        self.players = {} #ogni player ha un campo position per definire la posizione nel giro della partita
        self.host_id = None
        self.num_waiting_players = 0 #si tiene conto del numero di giocatori che sono in attesa di passare al livello successivo
        # il numero di players in attesa si incrementa ogni volta che viene ricevuto dal controller_server un nuovo messaggio che è stato completato un piatto

        self.curr_level = 0 #livello corrente a cui si è nella partita

    def add_player(self, player):
        if len(self.players) >= 8:
            return False
        
        self.players[player.id] = player
        player.room_code = self.code

        if self.host_id is None:
            self.host_id = player.id

        self._update_state()
        return True

    def remove_player(self, player_id):
        if player_id in self.players:
            self.removed_player = self.players.pop(player_id)
            if self.removed_player.position is not None:
                self._update_players_position_in_play(self.removed_player.position)
            return self.removed_player
        return None 
                
    def _update_state(self): #aggiorna lo stato della stanza in base ai giocatori
        if self.state in [RoomState.IN_GAME, RoomState.OVER]:
            return
        
        player_count = len(self.players)
        
        if player_count < 2:
            self.state = RoomState.INIT
        elif 2 <= player_count <= 8:
            self.state = RoomState.READY

    def set_in_game(self):
        self.state = RoomState.IN_GAME

    def check_all_waiting(self):
        return self.num_waiting_players > 0 and self.num_waiting_players >= len(self.players) - 1

    def set_random_players_position_in_play(self):
        list_players = list(self.players.values())
        for index, player in enumerate(list_players):
            player.position = index

    def set_players_position_in_play(self, players_pos_by_ingr_id):

        for pos, player_ingr_id in enumerate(players_pos_by_ingr_id):
            player = self._get_player_from_ingr_id(player_ingr_id)
            if player is not None:
                player.position = pos
            else:
                print(f"ATTENZIONE: Giocatore con ingrediente {player_ingr_id} non trovato nella stanza!")#debug
                print("id dei giocatori: ")
                for player in self.players.values():
                    print(player.ingr_id)
        for player in self.players.values():
            print(f"id: {player.ingr_id}, pos:{player.position}")   

    def _get_player_from_ingr_id(self, ingr_id):
        for player in self.players.values():
            if player.ingr_id == ingr_id:
                return player    
        return None
    
    #funzione che aggiorna il giro dei giocatori nella partita dopo che uno di essi è uscito
    def _update_players_position_in_play(self, removed_player_position):
        list_players = list(self.players.values())
        for player in list_players:
            #tutti i giocatori succesivi alla posizione del giocatore rimosso si spostano indietro di una posizione
            if player.position is not None and player.position > removed_player_position:
                player.position -= 1


    def get_near_player(self, current_player, side): #side è LEFT o RIGHT
        if side == "LEFT":
            near_position = (current_player.position - 1) % len(self.players)
        elif side == "RIGHT":
            near_position = (current_player.position + 1) % len(self.players)
        for player in self.players.values():
            print(f"id: {player.ingr_id}, pos:{player.position}")
            if player.position == near_position:
                return player
        return None    
    
    def advance_level(self):
        current_index = DIFFICULTY_ORDER.index(self.current_level)
        if current_index < len(DIFFICULTY_ORDER) - 1:
            self.current_level = DIFFICULTY_ORDER[current_index + 1]
            return self.current_level
        return None