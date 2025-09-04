from src.gameobjects.tile_object_base import TileObjectBase
from src.gameobjects.enums import ECategory, EPrerequisites

class TileObjectBuildable(TileObjectBase):
    def __init__(self, 
                 name : str, 
                 category : ECategory,
                 tileset_coord : int,
                 display_name : str, 
                 prerequisites : EPrerequisites, 
                 default_cost : int,
                 description : str):
        super().__init__(name, category, tileset_coord)
        self.__display_name : str = display_name
        self.__prerequisites : EPrerequisites = prerequisites
        self.__default_cost : int = default_cost
        self.__description : str = description

    @property
    def display_name(self):
        return self.__display_name
    
    @property
    def prerequisites(self):
        return self.__prerequisites
    
    @property
    def default_cost(self):
        return self.__default_cost
    
    @property
    def description(self):
        return self.__description
        