import pygame
from .base_state import BaseState

class LobbyState(BaseState):
    def __init__(self, model):
        super().__init__(model)
        #todo aggiungere lista dei giocatori e il loro stato di ready
        self.players_ready = []

    def handle_input(self, event, send_queue, model):
        pass

    def update(self):
        pass