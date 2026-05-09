import pygame
import json
from .base_state import BaseState

class AwaitJoinState(BaseState):
    def __init__(self, model):
        super().__init__(model)

    def handle_input(self, event, send_queue, model):
        #todo deve solo aspettare che il host della stanza avvia il gioco
        pass

    
    