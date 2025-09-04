from src.gamestates.interface_game_state import IGameState, EGameState
from src.saves.world_manager import WorldManager
from src.render.view import View

import pygame.event

class StateNormalBuildMode(IGameState):
    def __init__(self, world : WorldManager, view : View):
        self.world = world
        self.view = view

    def process_event(self, event : pygame.event, ignore : bool = False):
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left mouse button (pygame hasn't enum for this probably)
                    self.world.accept_suggestion()
            case pygame.MOUSEMOTION:
                x, y = event.pos
                self.world.suggest_placement(self.view.screen_to_world_coords(x, y))

    @staticmethod
    def enum():
        return EGameState.NORMAL_BUILD_MODE