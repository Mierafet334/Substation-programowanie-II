from src.gamestates.interface_game_state import IGameState, EGameState
from src.saves.world_manager import WorldManager
from src.render.view import View
import pygame

class StateSession(IGameState):
    def __init__(self, world : WorldManager, view : View):
        self.world = world
        self.view = view

    def process_event(self, event, ignore : bool = False):
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left mouse button (pygame hasn't enum for this probably)
                    x, y = event.pos
                    obj = self.world.get_object_from_coords(self.view.screen_to_world_coords(x, y))
                    print(obj)
                    if obj:
                        print(obj.tileset_coord, obj.name)

    @staticmethod
    def enum():
        return EGameState.SESSION