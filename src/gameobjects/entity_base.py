from src.gameobjects.tile_object_base import TileObjectBase

from typing import List

class EntityBase():
    def __init__(self,
                 name : str,
                 max_elements : int):
        self._name = name
        self._max_elements = max_elements

        self._tiles : List[TileObjectBase] = list()
        self._energy_grid = None

    @property
    def name(self):
        return self._name
    
    @property
    def max_elements(self):
        return self._max_elements
    
    @property
    def n_elements(self):
        return len(self._tiles)
    
    def get_tile(self, index):
        return self._tiles[index]
    
    def set_grid(self, new_grid):
        self._energy_grid = new_grid

    def add_object(self, object : TileObjectBase):
        self._tiles.append(object)
        object.entity = self