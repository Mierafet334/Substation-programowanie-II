from src.gameobjects.tile_object_db_iterator import TileObjectDBIterator
from src.gameobjects.tile_object_base import TileObjectBase
from src.gameobjects.tile_object_buildable import TileObjectBuildable
from src.gameobjects.power_plant_base import PowerPlantBase
from src.gameobjects.power_plant_unit import PowerPlantUnit
from src.gameobjects.consumer import Consumer
from src.gameobjects.power_plant_generic_element import PowerPlantGenericElement
from src.gameobjects.transmission_pylon import TransmissionPylon
from src.gameobjects.enums import *

import json
from copy import deepcopy
from pathlib import Path

class TileObjectDB():
    def __init__(self, path : Path):
        # Read object from json using custom decoder
        self.__data : dict[str, TileObjectBase] = dict()
        temp_data = None

        with open(path, "r") as file:
            temp_data = json.load(file, object_hook=self.__json_object_hook)

            for element in temp_data:
                self.__data[element.name] = element

    @staticmethod
    def __json_object_hook(dict):
        # Basic properties all objects must have
        name = dict["name"]
        category = dict["category"]
        tileset_coord = dict["tileset_coord"]

        # print("Found Tile category: {}, name: {}".format(category, name))

        match category:
            case "generic_consumer":
                min_consumption = float(dict["min_consumption"])
                max_consumption = float(dict["max_consumption"])
                time_variance = float(dict["time_variance"])
                corr_day_length = float(dict["corr_day_length"])
                corr_temperature = float(dict["corr_temperature"])
                return Consumer(name,  
                                       tileset_coord, 
                                       min_consumption, 
                                       max_consumption, 
                                       time_variance, 
                                       corr_day_length, 
                                       corr_temperature)
            case "power_plant_base":
                display_name = dict["display_name"]
                prerequisites = EPrerequisites.from_list(dict["prerequisites"])
                default_cost = float(dict["default_cost"])
                description = dict["description"]
                technology = ETechnology.from_string(dict["technology"])
                max_units = int(dict["max_units"])
                max_elements = int(dict["max_elements"])
                return PowerPlantBase(name,
                                      tileset_coord,
                                      display_name,
                                      prerequisites,
                                      default_cost,
                                      description,
                                      technology,
                                      max_units,
                                      max_elements)
            case "power_plant_unit":
                display_name = dict["display_name"]
                prerequisites = EPrerequisites.from_list(dict["prerequisites"])
                default_cost = float(dict["default_cost"])
                description = dict["description"]
                technology = ETechnology.from_string(dict["technology"])
                power_generation = float(dict["power_generation"])
                power_efficiency = float(dict["power_efficiency"])
                heat_efficiency = float(dict["heat_efficiency"])
                cost_of_operation = float(dict["cost_of_operation"])
                fail_rate = float(dict["fail_rate"])
                return PowerPlantUnit(name,
                                      tileset_coord,
                                      display_name,
                                      prerequisites,
                                      default_cost,
                                      description,
                                      technology,
                                      power_generation,
                                      power_efficiency,
                                      heat_efficiency,
                                      cost_of_operation,
                                      fail_rate)
            case "power_plant_generic_element":
                display_name = dict["display_name"]
                prerequisites = EPrerequisites.from_list(dict["prerequisites"])
                default_cost = float(dict["default_cost"])
                description = dict["description"]
                technology = ETechnology.from_string(dict["technology"])
                property_name = dict["property_name"]
                property_value = float(dict["property_value"])
                return PowerPlantGenericElement(name,
                                      tileset_coord,
                                      display_name,
                                      prerequisites,
                                      default_cost,
                                      description,
                                      technology,
                                      property_name,
                                      property_value)
            case "transmission_line":
                display_name = dict["display_name"]
                prerequisites = EPrerequisites.from_list(dict["prerequisites"])
                default_cost = float(dict["default_cost"])
                description = dict["description"]
                proper_admittance = complex(dict["proper_admittance"])
                max_length = int(dict["max_length"])
                return TransmissionPylon(name,
                                         tileset_coord,
                                         display_name,
                                         description,
                                         prerequisites,
                                         default_cost,
                                         proper_admittance,
                                         max_length)
            case "buildable_object":
                display_name = dict["display_name"]
                prerequisites = EPrerequisites.from_list(dict["prerequisites"])
                default_cost = float(dict["default_cost"])
                description = dict["description"]
                return TileObjectBuildable(name,
                                           ECategory.BUILDABLE_OBJECT,
                                           tileset_coord,
                                           display_name,
                                           prerequisites,
                                           default_cost,
                                           description)
            case _:
                raise KeyError("Unknown key in object category: {}".format(category))
    
    @classmethod
    def parse_dict_as_tile_object(cls, dict : dict):
        return cls.__json_object_hook(dict)
        

    def __iter__(self):
        # Iterator for all objects in database
        return TileObjectDBIterator(self.__data)
    
    def get_iter_by_category(self, filter : ECategory):
        # Iterator for objects in database with filering
        data = self.get_objects_by_category(filter)
        return TileObjectDBIterator(data)

    def get_objects_by_category(self, category : ECategory):
        filtered = list()
        for value in self.__data.values():
            if value.category == category:
                filtered.append(value)
        
        return filtered

    def get_tileobject_instance(self, name : str):
        return deepcopy(self.__data[name])