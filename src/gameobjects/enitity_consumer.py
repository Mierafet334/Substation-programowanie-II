from src.gameobjects.entity_energy_node import EntityEnergyNode
from src.gameobjects.consumer import Consumer

class EntityConsumer(EntityEnergyNode):
    def __init__(self,
                 name : str,
                 max_elements : int):
        super().__init__(name, max_elements)

        self.__energy_consumption = None
        self.__min_energy_consumption = None
        self.__max_energy_consumption = None
        self.__coeff_of_power = None
        self.__total_corr_temperature = None
        self.__total_corr_day_length = None
        self.__total_time_variance = None

    def add_object(self, object : Consumer):
        self._tiles.append(object)
        object.entity = self