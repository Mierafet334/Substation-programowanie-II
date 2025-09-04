from src.gameobjects.tile_object_buildable import TileObjectBuildable
from src.gameobjects.enums import *

class PowerPlantElement(TileObjectBuildable):
    def __init__(self, 
                 name : str,
                 category : ECategory,
                 tileset_coord : int,
                 display_name : str, 
                 prerequisites : EPrerequisites, 
                 default_cost : int,
                 description : str,
                 technology : ETechnology):
        super().__init__(name, category, tileset_coord, display_name, prerequisites, default_cost, description)
        self.__technology : ETechnology = technology
        self.__age : int = 0

    @property
    def technology(self):
        return self.__technology
    
    @property
    def age(self):
        return self.__age
