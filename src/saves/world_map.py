from src.config import Config
from src.render.region import Region
from src.gameobjects.enitity_consumer import EntityConsumer
from src.gameobjects.entity_base import EntityBase
from src.gameobjects.tile_object_db import TileObjectDB
from src.gameobjects.tile_object_base import TileObjectBase

import json
import numpy as np
from math import ceil, floor
from typing import List, Tuple

class WorldMap():
    def __init__(self, path : str):
        self.__map_height : int = None
        self.__map_width : int = None

        self.__entities : List[EntityBase] = list()
        self.__object_coords : List[Tuple[int, int, int, int, TileObjectBase]] = list()
        self.__terrain_regions : np.ndarray = None
        self.__object_regions : np.ndarray = None

        with open(path, "r") as file:
            json.load(file, object_hook=self.__json_object_hook)

    def __json_object_hook(self, dct : dict):
        if "type" in dct.keys() and dct["type"] != "":
            object_type = dct["type"]
        elif "data" in dct.keys():
            object_type = "chunk"
        elif "gid" in dct.keys():
            object_type = "tile_object"
        elif "firstgid" in dct.keys() and "source" in dct.keys():
            object_type = "tileset"
        else:
            print(dct.keys())
            raise KeyError

        match object_type:
            case "map":
                return self.__parse_map(dct)
            case "tilelayer":
                return self.__parse_tilelayer(dct)
            case "objectgroup":
                return self.__parse_objectgroup(dct)
            case "tile_object":
                return self.__parse_tile_object(dct)
            case "tileset":
                pass # ignore tileset data, it is not important
            case "chunk":
                return self.__parse_chunk(dct)
            case "string":
                return self.__parse_property(dct)
            case "int":
                return self.__parse_property(dct)
            case "float":
                return self.__parse_property(dct)
            case _:
                print(dct.keys())
                raise KeyError("WorldMap: JSON object hook: Invalid type {}".format(object_type))

    def __parse_map(self, dct : dict):
        # Top level parser. Does not return object but sets class fields
        self.__map_height = ceil(int(dct["height"]) / Config.REGION_SIZE)
        self.__map_width = ceil(int(dct["width"] / Config.REGION_SIZE))

        terrain : List[Region] = None

        for element in dct["layers"]:
            if isinstance(element, WorldMapTilelayer):
                terrain = element.regions
            elif isinstance(element, EntityBase):
                self.__entities.append(element)
            else:
                raise Exception("WorldMap: map parser: unknown element type {}".format(type(element)))

        self.__terrain_regions = np.ndarray((self.__map_width, self.__map_height), dtype=Region)
        self.__object_regions = np.ndarray((self.__map_width, self.__map_height), dtype=Region)

        for reg in terrain:
            x, y = reg.world_pos
            self.__terrain_regions[x, y] = reg
            self.__object_regions[x, y] = Region((x, y))

        temp_object_coords = np.ndarray((self.__map_width, self.__map_height, Config.REGION_SIZE, Config.REGION_SIZE), dtype=Region)
        for coords in self.__object_coords:
            rx, ry, lx, ly, obj = coords

            self.__object_regions[rx, ry].set_offset((lx, ly), obj.tileset_coord)
            temp_object_coords[rx, ry, lx, ly] = obj

        self.__object_coords = temp_object_coords

        # Can be expanded to read other fields to validate the map file

    def __parse_tilelayer(self, dct : dict):
        width = int(dct["width"])
        height = int(dct["height"])
        regions = dct["chunks"]
        return WorldMapTilelayer(width, height, regions)

    def __parse_objectgroup(self, dct : dict):
        entity_class = dct["class"]

        match entity_class:
            case "consumer":
                name = dct["name"]
                max_elements = self.__get_named_property(dct["properties"], "max_elements")
                entity = EntityConsumer(name, max_elements)

                for object in dct["objects"]:
                    entity.add_object(object)

                return entity
            case _:
                pass # No other entity classes should be loaded from JSON

    def __parse_tile_object(self, dct : dict):
        x = int(dct["x"])
        y = int(dct["y"])

        # y coordinate has to be offset by tile size for Tiled assumes 
        # tile origin is in the lower left corner with y inccreasing downwards
        region_x = floor(x / Config.REGION_SIZE / Config.TILE_SIZE)
        region_y = -1 * floor((y - Config.TILE_SIZE) / Config.REGION_SIZE / Config.TILE_SIZE) # Minus corrects region ordering between game and Tiled

        local_x = floor(x / Config.REGION_SIZE - region_x * Config.REGION_SIZE)
        local_y = floor((y - Config.TILE_SIZE) / Config.REGION_SIZE + region_y * Config.REGION_SIZE)

        properties = self.__property_list_to_dict(dct["properties"])
        if properties["category"] == "generic_consumer":
            obj = TileObjectDB.parse_dict_as_tile_object(properties)
            self.__object_coords.append((region_x, region_y, local_x, Config.REGION_SIZE - local_y - 1, obj))
            return obj

    def __parse_chunk(self, dct : dict):
        data = dct["data"]
        height = int(dct["height"])
        width = int(dct["width"])
        x = int(dct["x"])
        y = int(dct["y"])

        if height != width or height != Config.REGION_SIZE:
            raise Exception("WorldMap: chunk parser: height ({}) or width ({}) is not equal to REGION_SIZE".format(height, width))
        
        x = int(x / Config.REGION_SIZE)
        y = int(y / Config.REGION_SIZE)

        data = np.array(data, dtype=np.int32)
        data -= np.ones(shape=data.shape, dtype=np.int32) # adjustment factor because in Tiled gid begins with 1 but in game it begins with 0
        return Region((x, -y), data)

    def __parse_property(self, dct : dict):
        return WorldMapProperty(dct["name"], dct["type"], dct["value"])
    
    @staticmethod
    def __get_named_property(property_list : List, name : str):
        for element in property_list:
            if element.name == name:
                return element.value
    
    @staticmethod
    def __property_list_to_dict(properties : List):
        result = dict()

        for element in properties:
            result[element.name] = element.value

        return result
    
    @property
    def entities(self):
        return self.__entities
    
    @property
    def terrain_regions(self):
        return self.__terrain_regions
    
    @property
    def object_regions(self):
        return self.__object_regions
    
    @property
    def object_coords(self):
        return self.__object_coords
    
    @property
    def world_width(self):
        return self.__map_width
    
    @property
    def world_height(self):
        return self.__map_height

class WorldMapTilelayer():
    def __init__(self, width : int, height : int, regions : List[Region]):
        self.__width = int(width / Config.REGION_SIZE)
        self.__height = int(height / Config.REGION_SIZE)

        if self.__width != width/Config.REGION_SIZE:
            raise Exception("WorldMap: tilelayer: width {} is not multiple of REGION_SIZE".format(width))
        
        if self.__height != height/Config.REGION_SIZE:
            raise Exception("WorldMap: tilelayer: height {} is not multiple of REGION_SIZE".format(width))
        
        self.__regions = regions

    @property
    def width(self):
        return self.__width
    
    @property
    def height(self):
        return self.__height
    
    @property
    def regions(self):
        return self.__regions

class WorldMapProperty():
    def __init__(self, name : str, type : str, value : str | int | float):
        self.__name = name
        match type:
            case "string":
                self.__value = str(value)
            case "float":
                self.__value = float(value)
            case "int":
                self.__value = int(value)
            case _:
                raise TypeError("WorldMap: property parser: unknown property type {}".format(type))
            
    @property
    def name(self):
        return self.__name
    
    @property
    def value(self):
        return self.__value