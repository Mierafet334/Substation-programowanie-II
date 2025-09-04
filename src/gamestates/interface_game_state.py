from abc import ABC, abstractmethod
import pygame
from enum import Enum, auto

class EGameState(Enum):
    SESSION = auto()
    NORMAL_BUILD_MODE = auto()
    SPLINE_BUILD_MODE = auto()
    MAIN_MENU = auto()
    MANAGEMENT_MODE = auto()

class IGameState(ABC):
    @abstractmethod
    def process_event(self, event : pygame.event, ignore : bool = False):
        pass
    
    @staticmethod
    @abstractmethod
    def enum():
        pass