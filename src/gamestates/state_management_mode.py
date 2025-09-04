from src.gamestates.interface_game_state import IGameState, EGameState

class StateManagementMode(IGameState):
    def __init__(self):
        pass

    def process_event(self, event, ignore : bool = False):
        pass

    @staticmethod
    def enum():
        return EGameState.MANAGEMENT_MODE