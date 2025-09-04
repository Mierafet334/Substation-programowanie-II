from src.gameobjects.tile_object_buildable import TileObjectBuildable
from src.gameobjects.enums import *

class TransmissionPylon(TileObjectBuildable):
    def __init__(self, 
                 name : str, 
                 tileset_coord : int,
                 display_name : str, 
                 description : str,
                 prerequisites : EPrerequisites, 
                 default_cost : int,
                 proper_admittance : complex,
                 max_length : int):
        super().__init__(name, ECategory.TRANSMISSION_LINE, tileset_coord, display_name, prerequisites, default_cost, description)
        self.__proper_admittance : complex = proper_admittance
        self.__max_length : int = max_length
    
    @property
    def proper_admittance(self):
        return self.__proper_admittance
    
    @property
    def max_length(self):
        return self.__max_length
