from src.gameobjects.power_plant_element import PowerPlantElement
from src.gameobjects.enums import *

class PowerPlantUnit(PowerPlantElement):
    def __init__(self, 
                 name : str, 
                 tileset_coord : int,
                 display_name : str, 
                 prerequisites : EPrerequisites, 
                 default_cost : int,
                 description : str,
                 technology : ETechnology,
                 power_generation : float,
                 power_efficiency : float,
                 heat_efficiency : float,
                 cost_of_operation : float,
                 fail_rate : float):
        super().__init__(name, ECategory.POWER_PLANT_UNIT, tileset_coord, display_name, prerequisites, default_cost, description, technology)
        self.power_generation = power_generation
        self.power_efficiency = power_efficiency
        self.heat_efficiency = heat_efficiency
        self.cost_of_operation = cost_of_operation
        self.fail_rate = fail_rate