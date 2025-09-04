from enum import Enum, Flag, auto
from typing import List

class ECategory(Enum):
    TERRAIN = auto()
    POWER_PLANT_BASE = auto()
    POWER_PLANT_GENERIC_ELEMENT = auto()
    POWER_PLANT_UNIT = auto()
    TRANSMISSION_LINE = auto()
    BUILDABLE_OBJECT = auto()
    CONSUMER = auto()

    @classmethod
    def from_string(cls, string : str):
        match string:
            case "terrain":
                return cls.TERRAIN
            case "power_plant_base":
                return cls.POWER_PLANT_BASE
            case "power_plant_generic_element":
                return cls.POWER_PLANT_GENERIC_ELEMENT
            case "power_plant_unit":
                return cls.POWER_PLANT_UNIT
            case "transmission_line":
                return cls.TRANSMISSION_LINE
            case "buildable_object":
                return cls.BUILDABLE_OBJECT
            case "consumer":
                return cls.CONSUMER
            case _:
                raise KeyError("Unknown key for category enum: {}".format(string))

class EPrerequisites(Flag):
    NONE = 0
    BUILDABLE = auto()
    ADJACENT_ENTITY = auto()
    ADJACENT_POWER_NODE = auto()
    SAME_TECHNOLOGY = auto()
    NO_ADJACENT_ENTITIES = auto()

    @classmethod
    def from_list(cls, list : List[str]):
        result = cls.NONE
        for element in list:
            match element:
                case "buildable":
                    result = result | cls.BUILDABLE
                case "adjacent_entity":
                    result = result | cls.ADJACENT_ENTITY
                case "adjacent_grid_node":
                    result = result | cls.ADJACENT_POWER_NODE
                case "same_technology":
                    result = result | cls.SAME_TECHNOLOGY
                case "no_adjacent_entities":
                    result = result | cls.NO_ADJACENT_ENTITIES
                case _:
                    raise KeyError("Unknown key for category enum: {}".format(element))
        return result
        

class ETechnology(Enum):
    UNIVERSAL = auto()
    COAL = auto()
    SOLAR = auto()
    NUCLEAR = auto()

    def __str__(self):
        return self.name.capitalize()

    @classmethod
    def from_string(cls, string : str):
        match string:
            case "universal":
                return cls.UNIVERSAL
            case "coal":
                return cls.COAL
            case "solar":
                return cls.SOLAR
            case "nuclear":
                return cls.NUCLEAR
            case _:
                raise KeyError("Unknown key for technology enum: {}".format(string))