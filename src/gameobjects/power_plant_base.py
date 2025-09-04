from src.gameobjects.power_plant_element import PowerPlantElement
from src.gameobjects.enums import *

class PowerPlantBase(PowerPlantElement):
    def __init__(self, 
                 name : str,
                 tileset_coord : int,
                 display_name : str, 
                 prerequisites : EPrerequisites, 
                 default_cost : int,
                 description : str,
                 technology : ETechnology,
                 max_units : int,
                 max_elements : int):
        super().__init__(name, ECategory.POWER_PLANT_BASE, tileset_coord, display_name, prerequisites, default_cost, description, technology)
        self.max_units = max_units
        self.max_elements = max_elements