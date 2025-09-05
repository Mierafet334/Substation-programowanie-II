from src.render.shader_program import ShaderProgram
from src.saves.world_map import WorldMap
from src.gameobjects.entity_base import EntityBase
from src.gameobjects.tile_object_buildable import TileObjectBuildable
from src.gameobjects.tile_object_base import TileObjectBase
from src.gameobjects.entity_energy_node import EntityEnergyNode
from src.gameobjects.entity_power_plant import EntityPowerPlant
from src.gameobjects.entity_transmission_line import EntityTransmissionLine
from src.gameobjects.entity_substation import EntitySubstation
from src.gameobjects.power_plant_base import PowerPlantBase
from src.gameobjects.entity_coal_power_plant import EntityCoalPowerPlant
from src.gameobjects.transmission_pylon import TransmissionPylon
from src.gameobjects.power_plant_element import PowerPlantElement
from src.colors import Colors
from src.config import Config
from src.gameobjects.enums import *

from typing import Tuple, List
from pathlib import Path
import numpy as np

WorldCoord = Tuple[int, int, int, int]

class WorldManager():
    def __init__(self, world_map : WorldMap):

        self.__world_map = world_map

        self.__energy_grids : List = list() # TODO
        self.__entities : List[EntityBase] = world_map.entities
        
        self.__all_regions : np.ndarray = world_map.terrain_regions
        self.__all_object_regions : np.ndarray = world_map.object_regions
        self.__object_coords : np.ndarray = world_map.object_coords
        
        self.__last_suggested_object : TileObjectBuildable = None
        self.__last_suggested_object_coords : WorldCoord = None
        self.__last_suggested_object_saved_tileset_offset : int = None
        self.__last_suggested_object_valid : bool = True

        self.__player_money : float = Config.PLAYER_START_MONEY

        self.__object_counters : dict = {"power_plant" : 0, "transmission_line" : 0, "substation" : 0}
    
    @classmethod
    def from_map_file(cls, path : Path):
        return cls(WorldMap(path))
    
    @property
    def last_suggested_object(self):
        return self.__last_suggested_object
    
    @last_suggested_object.setter
    def last_suggested_object(self, new_object : TileObjectBuildable):
        self.__last_suggested_object = new_object

    def add_tile_object(self, coords : WorldCoord, obj : TileObjectBuildable):
        self.__object_coords[coords[0], coords[1], coords[2], coords[3]] = obj
        self.__all_object_regions[coords[0], coords[1]].set_offset((coords[2], coords[3]), obj.tileset_coord)

    def add_entity(self, entity : EntityBase):
        self.__entities.append(entity)

    def get_object_from_coords(self, coords: WorldCoord) -> TileObjectBuildable:
        return self.__object_coords[coords[0], coords[1], coords[2], coords[3]]

    def get_entity_from_coords(self, coords: WorldCoord) -> EntityBase:
        obj = self.get_object_from_coords(self, coords)
        if obj:
            return obj.entity
        else:
            return None

    def suggest_placement(self, coords: WorldCoord):
        # Check prerequisites of __last_suggested_object (if not None), color accordingly, if valid allow placement
        if self.__last_suggested_object:
            # Retrieive last modified tileset offset and restore it to previous state
            last_coords = self.__last_suggested_object_coords
            if last_coords:
                self.__all_object_regions[last_coords[0], last_coords[1]].set_offset((last_coords[2], last_coords[3]), self.__last_suggested_object_saved_tileset_offset)
                self.__all_object_regions[last_coords[0], last_coords[1]].set_highlight((last_coords[2], last_coords[3]), Colors.NONE)

            # Save state of offset and modify it later
            self.__last_suggested_object_coords = coords
            self.__last_suggested_object_saved_tileset_offset = self.__all_object_regions[coords[0], coords[1]].get_offset((coords[2], coords[3]))
            self.__all_object_regions[coords[0], coords[1]].set_offset((coords[2], coords[3]), self.__last_suggested_object.tileset_coord)

            self.__last_suggested_object_valid = self.__check_placement_validity(self.__last_suggested_object.prerequisites)

            if not self.__last_suggested_object_valid:
                self.__all_object_regions[coords[0], coords[1]].set_highlight((coords[2], coords[3]), Colors.WRONG_PLACEMENT)

    def __check_placement_validity(self, prerequisites : EPrerequisites) -> bool:
        rx, ry, lx, ly = self.__last_suggested_object_coords

        world_height = self.__world_map.world_height
        world_width = self.__world_map.world_width

        world_upper_bound =  (world_height - 1)/2
        world_lower_bound = -(world_height - 1)/2
        world_left_bound =  -(world_width - 1)/2
        world_right_bound =  (world_width - 1)/2

        neighbours = list()

        result = EPrerequisites.NONE

        if lx + 1 >= Config.REGION_SIZE:
            if rx + 1 > world_right_bound:
                return False
            else:
                neighbours.append(self.__object_coords[rx + 1, ry, 0, ly])
        else:
            neighbours.append(self.__object_coords[rx, ry, lx + 1, ly])

        if lx - 1 < 0:
            if rx - 1 < world_left_bound:
                return False
            else:
                neighbours.append(self.__object_coords[rx - 1, ry, Config.REGION_SIZE - 1, ly])
        else:
            neighbours.append(self.__object_coords[rx, ry, lx - 1, ly])

        if ly + 1 >= Config.REGION_SIZE:
            if ry + 1 > world_upper_bound:
                return False
            else:
                neighbours.append(self.__object_coords[rx, ry + 1, rx, 0])
        else:
            neighbours.append(self.__object_coords[rx, ry, lx, ly + 1])

        if ly - 1 < 0:
            if ry - 1 < world_lower_bound:
                return False
            else:
                neighbours.append(self.__object_coords[rx, ry - 1, rx, Config.REGION_SIZE - 1])
        else:
            neighbours.append(self.__object_coords[rx, ry, lx, ly - 1])

        for tile in neighbours:
            tile : TileObjectBase

            if not tile:
                continue

            if isinstance(tile.entity, EntityBase):
                result |= EPrerequisites.ADJACENT_ENTITY
            
            if isinstance(tile.entity, EntityEnergyNode):
                result |= EPrerequisites.ADJACENT_POWER_NODE
            
            if isinstance(tile.entity, EntityPowerPlant):
                if isinstance(self.__last_suggested_object, PowerPlantElement):
                    if tile.entity.technology == self.__last_suggested_object.technology:
                        result |= EPrerequisites.SAME_TECHNOLOGY

        if self.__all_regions[rx, ry].get_offset((lx, ly)) == 1 and self.__object_coords[rx, ry, lx, ly] == None:
            result |= EPrerequisites.BUILDABLE

        if not result & EPrerequisites.ADJACENT_ENTITY:
            result |= EPrerequisites.NO_ADJACENT_ENTITIES

        return result == prerequisites

    def accept_suggestion(self):
        lso = self.__last_suggested_object
        if lso:

            if not self.__last_suggested_object_valid:
                return
            
            self.__player_money -= lso.default_cost

            coords = self.__last_suggested_object_coords
            self.__last_suggested_object_saved_tileset_offset = lso.tileset_coord # Without it tile is overwritten by last known tileset offset in that place
            self.add_tile_object(coords, lso)

            if lso.category == ECategory.POWER_PLANT_BASE:
                lso : PowerPlantBase
                if lso.technology == ETechnology.COAL:
                    entity = EntityCoalPowerPlant("Power Plant #{}".format(self.__object_counters["power_plant"] + 1), lso.max_elements, lso.max_units)
                entity.add_object(lso)
                self.__entities.append(entity)
                self.__object_counters["power_plant"] += 1

            if lso.category == ECategory.BUILDABLE_OBJECT and lso.name == "substation":
                lso : EntitySubstation
                entity = EntitySubstation("Substation #{}".format(self.__object_counters["substation"] + 1))
                entity.add_object(lso)
                self.__entities.append(entity)
                self.__object_counters["substation"] += 1

    def accept_suggestion_spline(self, in_node : int, out_node : int):
        # TODO implement spline build mode
        lso = self.__last_suggested_object
        if lso:

            if not self.__last_suggested_object_valid:
                return

            coords = self.__last_suggested_object_coords
            self.__last_suggested_object_saved_tileset_offset = lso.tileset_coord # Without it tile is overwritten by last known tileset offset in that place
            self.add_tile_object(coords, lso)
            
            if lso.category == ECategory.TRANSMISSION_LINE:
                lso : TransmissionPylon
                self.__entities.append(EntityTransmissionLine("Transmission Line #{}".format(self.__object_counters["transmission_line"] + 1), lso.max_length, in_node, out_node))
                self.__object_counters["transmission_line"] += 1


    def get_world_bounds(self):
        width = self.__world_map.world_width
        height = self.__world_map.world_height

        return (-width/2 + 0.5, width/2 + 0.5, height/2 + 0.5, -height/2 + 0.5)
    
    def get_current_player_money(self) -> int:
        return self.__player_money

    def draw(self, shader : ShaderProgram):
        for region in self.__all_regions.flatten():
            region.draw(shader)

        for region in self.__all_object_regions.flatten():
            region.draw(shader)

    def destroy(self):
        for region in self.__all_regions.flatten() :
            region.destroy()