from .states.menu_state import MenuState
from .states.lobby_state import LobbyState
from .states.join_state import JoinState
from .states.playing_state import PlayingState
from .states.await_join_state import AwaitJoinState
from .states.scoreboard_state import ScoreboardState

class GameModel:
    def __init__(self):
        self.game_code = ""
        self.player_id = ""
        self.ingr_id = ""
        self.error_message = ""
        
        # Dizionario degli stati
        self.states = {
            "MENU": MenuState(self),
            "LOBBY": LobbyState(self),
            "JOIN_INPUT": JoinState(self),
            "AWAIT_JOIN": AwaitJoinState(self),
            "PLAYING": PlayingState(self),
            "SCORE": ScoreboardState(self)
        }
        #to do rimpostare a MENU
        self.current_state_key = "MENU"

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