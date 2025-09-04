from src.gameobjects.enums import ECategory, EPrerequisites

class TileObjectBase():
    def __init__(self, 
                 name : str, 
                 category : ECategory, 
                 tileset_coord : int):
        self.__name : str = name
        self.__category : ECategory = category
        self.__tileset_coord : int = tileset_coord
        self.__entity = None

    def __next__(self):
        pass

    @property
    def name(self):
        return self.__name
    
    @property
    def category(self):
        return self.__category
    
    @property
    def tileset_coord(self):
        return self.__tileset_coord
    
    @property
    def entity(self):
        return self.__entity
    
    @entity.setter
    def entity(self, new_entity):
        self.__entity = new_entity
