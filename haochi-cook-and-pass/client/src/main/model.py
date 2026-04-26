from .states.menu_state import MenuState
from .states.lobby_state import LobbyState
from .states.join_state import JoinState
from .states.playing_state import PlayingState

class GameModel:
    def __init__(self):
        self.game_code = ""
        self.player_id = ""
        
        # Dizionario degli stati
        self.states = {
            "MENU": MenuState(self),
            "LOBBY": LobbyState(self), #todo
            "JOIN_INPUT": JoinState(self), #todo
            "PLAYING": PlayingState(self)
        }
        #to do rimpostare a MENU
        self.current_state_key = "MENU" #"PLAYING"

    @property
    def current_state(self):
        return self.states[self.current_state_key]

    def set_state(self, state_key):
        if state_key in self.states:
            self.current_state_key = state_key

    def switch_to(self, state_key):
        if state_key in self.states:
            self.current_state_key = state_key
        else:
            raise ValueError(f"Stato {state_key} non esiste")