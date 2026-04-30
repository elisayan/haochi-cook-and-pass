import uuid

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

    def add_player(self, player):
        if len(self.players) >= 8:
            #raise Exception("Room full")
            return False
        
        self.players[player.id] = player
        player.room_code = self.code

        if self.host_id is None:
            self.host_id = player.id

        self._update_state()
        return True

    def remove_player(self, player_id):
        removed_player_position = self.players[player_id].position
        if player_id in self.players:
            del self.players[player_id]
            
        # se era host, assegna nuovo host (il primo rimasto) o None se vuota
        if player_id == self.host_id and self.players:
            self.host_id = next(iter(self.players.keys()))
        elif not self.players:
            self.host_id = None

        #si aggiorna il giro dopo che uno dei giocatori è stato rimosso
        self._update_players_position_in_play(removed_player_position)
        self._update_state()

    def _update_state(self): #aggiorna lo stato della stanza in base ai giocatori
        if self.state in [RoomState.IN_GAME, RoomState.OVER]:
            return  # non cambiare stato durante la partita
        
        player_count = len(self.players)
        
        if player_count < 2:
            self.state = RoomState.INIT
        elif 2 <= player_count <= 8:
            self.state = RoomState.READY

    #settata in modo casuale TO DO fare settare il giro al creatore della stanza 
    def set_players_position_in_play(self):
        list_players = list(self.players.values())
        for index, player in enumerate(list_players):
            player.position = index

    #funzione che aggiorna il giro dei giocatori nella partita dopo che uno di essi è uscito
    def _update_players_position_in_play(self, removed_player_position):
        list_players = list(self.players.values())
        for player in list_players:
            #tutti i giocatori succesivi alla posizione del giocatore rimosso si spostano indietro di una posizione
            if player.position > removed_player_position:
                player.position = player.position - 1


    def get_near_player(self, current_player, side): #side è LEFT o RIGHT
        if side == "LEFT":
            near_position = (current_player.position - 1) % len(self.players)
        elif side == "RIGHT":
            near_position = (current_player.position + 1) % len(self.players)
        for player in self.players.values():
            if player.position == near_position:
                return player
        return None    