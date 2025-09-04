from src.gameobjects.entity_base import EntityBase

class EntityEnergyNode(EntityBase):
    def __init__(self,
                 name : str,
                 max_elements : int):
        super().__init__(name, max_elements)
        self._voltage : float = 0
        self._updated : bool = False

    @property
    def voltage(self):
        return self._voltage
    
    @property
    def updated(self):
        return self._updated