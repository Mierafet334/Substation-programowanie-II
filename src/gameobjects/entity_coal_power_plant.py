from src.gameobjects.entity_power_plant import EntityPowerPlant
from src.gameobjects.enums import *

class EntityCoalPowerPlant(EntityPowerPlant):
    def __init__(self,
                 name : str,
                 max_elements : int,
                 max_units : int):
        super().__init__(name, max_elements, max_units, ETechnology.COAL)

        self.__total_efficiency : float = 0.0
        self.__stored_coal : float = 0.0
        self.__coal_intake : float = 0.0
        self.__cooling_capacity : float = 0.0

    @property
    def total_efficiency(self):
        return self.__total_efficiency
    
    @property
    def stored_coal(self):
        return self.__stored_coal
    
    @property
    def coal_intake(self):
        return self.__coal_intake
    
    @property
    def cooling_capacity(self):
        return self.__cooling_capacity
    
    @property
    def operational(self):
        return False