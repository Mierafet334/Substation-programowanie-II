from src.gamestates.interface_game_state import IGameState, EGameState
from src.saves.world_manager import WorldManager
from src.render.view import View

class StateSplineBuildMode(IGameState):
    def __init__(self, world : WorldManager, view : View):
        self.world = world
        self.view = view
    
    def process_event(self, event, ignore : bool = False):
        # TODO
        pass

    @staticmethod
    def enum():
        return EGameState.SPLINE_BUILD_MODE