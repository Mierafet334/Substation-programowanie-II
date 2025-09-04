from src.gameobjects.entity_base import EntityBase
from src.gameobjects.transmission_pylon import TransmissionPylon

class EntityTransmissionLine(EntityBase):
    def __init__(self,
                 name : str,
                 max_elements : int,
                 in_node : int,
                 out_node : int):
        super().__init__(name, max_elements)
        self.__in_node : int = in_node
        self.__out_node : int = out_node
        self.__admittance : complex = 0 + 0j
        self.__total_length : float = 0.0
        self.__current : float = 0.0
        self.__active : bool = True

    @property
    def connections(self):
        return [self.__in_node, self.__out_node]
    
    @property
    def admittance(self):
        return self.__admittance
    
    @property
    def total_length(self):
        return self.__total_length
    
    @property
    def current(self):
        return self.__current
    
    @property
    def active(self):
        return self.__active
    
    @active.setter
    def active(self, state : bool):
        self.__active = state
    
    def activate(self):
        self.__active = True

    def deactivate(self):
        self.__active = False

    def add_segment(self, segment : TransmissionPylon):
        #TODO add support for variable length segments
        self.__admittance += segment.proper_admittance