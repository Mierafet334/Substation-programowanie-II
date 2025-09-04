from src.gameobjects.entity_energy_node import EntityEnergyNode
from src.gameobjects.enums import *

from abc import abstractmethod

class EntityPowerPlant(EntityEnergyNode):
    def __init__(self,
                 name : str,
                 max_elements : int,
                 max_units : int,
                 technology : ETechnology,):
        super().__init__(name, max_elements)

        self._max_units : int = max_units
        self._technology : ETechnology = technology

        self._max_avail_power : float = 0.0
        self._min_avail_power : float = 0.0
        self._n_units : int = 0
        self._active : bool = False
        self._total_cost_of_operation : float = 0.0

    @property
    def max_units(self):
        return self._max_units
    
    @property
    def technology(self):
        return self._technology
    
    @property
    def max_avail_power(self):
        self._max_avail_power

    @property
    def min_avail_power(self):
        self._min_avail_power

    @property
    def n_units(self):
        return self._n_units
    
    @property
    def active(self):
        return self._active
    
    @property
    def cost_of_operation(self):
        return self._total_cost_of_operation
    
    @property
    @abstractmethod
    def operational(self) -> bool:
        # Check if all prerequisites are met
        pass