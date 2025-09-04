from src.gamestates.interface_game_state import IGameState, EGameState

class StateMenu(IGameState):
    def __init__(self):
        pass

    def process_event(self, event, ignore : bool = False):
        return
    
    @staticmethod
    def enum():
        return EGameState.MAIN_MENU