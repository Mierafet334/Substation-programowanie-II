from src.gameobjects.entity_energy_node import EntityEnergyNode
from src.gameobjects.enums import *

class EntitySubstation(EntityEnergyNode):
    def __init__(self,
                 name : str):
        super().__init__(name, 4)

        self.__connections : List[int] = list()