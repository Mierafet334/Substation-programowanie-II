from src.gameobjects.power_plant_element import PowerPlantElement
from src.gameobjects.enums import *

class PowerPlantGenericElement(PowerPlantElement):
    def __init__(self, 
                 name : str,  
                 tileset_coord : int,
                 display_name : str, 
                 prerequisites : EPrerequisites, 
                 default_cost : int,
                 description : str,
                 technology : ETechnology,
                 property_name : str,
                 property_value : float):
        super().__init__(name, ECategory.POWER_PLANT_GENERIC_ELEMENT, tileset_coord, display_name, prerequisites, default_cost, description, technology)
        self.property_name = property_name
        self.property_value = property_value