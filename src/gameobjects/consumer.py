from src.gameobjects.tile_object_base import TileObjectBase
from src.gameobjects.enums import *

class Consumer(TileObjectBase):
    def __init__(self, 
                 name : str,
                 tileset_coord : int, 
                 min_consumption : float,
                 max_consumption : float,
                 time_variance : float,
                 corr_day_length : float,
                 corr_temperature : float):
        super().__init__(name, ECategory.CONSUMER, tileset_coord)
        self.min_consumption : float = min_consumption
        self.max_consumption : float = max_consumption
        self.time_variance : float = time_variance
        self.corr_day_length : float = corr_day_length
        self.corr_temperature : float = corr_temperature