from imgui.integrations.pygame import PygameRenderer
from src.render.view import View
from src.saves.world_manager import WorldManager
from src.gameobjects.tile_object_db import TileObjectDB
from src.gameobjects.tile_object_base import TileObjectBase
from src.gameobjects.tile_object_buildable import TileObjectBuildable
from src.gamestates.interface_game_state import EGameState, IGameState
from src.gameobjects.enums import *
from src.gamestates import *
from src.config import Config
from src.colors import Colors

import imgui, pygame
from enum import Enum, auto

FRAME_HEIGHT = 20 + 2 * 3 # ImGui constant, not configurable so is not present in src/config.py

class GUIState(Enum):
    NORMAL = auto()
    BUILD_MENU_ACTIVE = auto()
    MANAGE_MENU_ACTIVE = auto()
    MAIN_MENU = auto()
    EXIT_MODAL_MENU = auto()

class GUI:
    def __init__(self, size_x : int, size_y : int, view : View, world : WorldManager, state : IGameState, db : TileObjectDB):
        imgui.create_context()
        self.impl = PygameRenderer()
        io = imgui.get_io()
        io.display_size = (size_x, size_y)
        self.io = io

        new_font = io.fonts.add_font_from_file_ttf("./src/font/Jersey10-Regular.ttf", 20,)
        self.impl.refresh_font_texture()

        self.font = new_font

        self.view = view
        self.world = world
        self.game_state = state
        self.tile_db = db

        self.gui_state = GUIState.NORMAL

        self.selected = None
        self.selected_category = None

        self.style = imgui.get_style()
        self.__init__style()

    def process_event(self, event):
        self.impl.process_event(event)

    def process_inputs(self):
        self.impl.process_inputs()

    def draw(self):
        imgui.new_frame()
        imgui.push_font(self.font)

        if self.gui_state != GUIState.MAIN_MENU and self.gui_state != GUIState.EXIT_MODAL_MENU:
            self.__draw_status_bar()

        if self.gui_state == GUIState.NORMAL:
            self.__draw_menu()

        if self.gui_state == GUIState.BUILD_MENU_ACTIVE:
            self.__draw_build_menu()

        if self.gui_state == GUIState.EXIT_MODAL_MENU:
            self.__draw_exit_menu()

        if self.gui_state == GUIState.MANAGE_MENU_ACTIVE:
            self.__draw_manage_menu()

        imgui.pop_font()

    def __draw_menu(self):
        imgui.begin("Menu", False, imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_RESIZE)
        center_x = self.io.display_size[0]/2 - imgui.get_window_width()/2
        height_y = self.io.display_size[1]
        
        if imgui.is_window_collapsed():
            imgui.set_window_position(center_x, height_y - FRAME_HEIGHT)
        else:
            imgui.set_window_position(center_x, height_y - imgui.get_window_height())

        imgui.set_window_size(220, 80)

        if imgui.button("Build", width=60, height=35):
            self.gui_state = GUIState.BUILD_MENU_ACTIVE
            self.game_state = StateNormalBuildMode(self.world, self.view)

        imgui.same_line(80)

        if imgui.button("Manage", width=60, height=35):
            self.gui_state = GUIState.MANAGE_MENU_ACTIVE
            self.game_state = StateManagementMode()

        imgui.same_line(150)
        
        if imgui.button("Exit", width=60, height=35):
            self.gui_state = GUIState.EXIT_MODAL_MENU
            self.game_state = StateMenu()

        imgui.end()


    def __draw_build_menu(self):
        window_open = imgui.begin("Build menu", True, imgui.WINDOW_NO_RESIZE)[1]
        imgui.set_window_size(Config.GUI_BUILD_MENU_WIDTH, Config.GUI_BUILD_MENU_HEIGHT)

        width = imgui.get_window_content_region_width()

        imgui.text("Select object to build: ")

        if imgui.tree_node("Power Plant Bases"):
            for entry in self.tile_db.get_iter_by_category(ECategory.POWER_PLANT_BASE):
                self.__draw_build_selector_tile(entry, width)
                if imgui.is_item_hovered():
                    self.__draw_build_tooltip_header(entry)
                    imgui.text("Technology: {}".format(entry.technology))
                    imgui.text("Maximum units: {}".format(entry.max_units))
                    imgui.text("Maximum elements: {}".format(entry.max_elements))
                    self.__draw_build_tooltip_footer(entry)
            imgui.tree_pop()

        if imgui.tree_node("Power Plant Units"):
            for entry in self.tile_db.get_iter_by_category(ECategory.POWER_PLANT_UNIT):
                self.__draw_build_selector_tile(entry, width)
                if imgui.is_item_hovered():
                    self.__draw_build_tooltip_header(entry)
                    imgui.text("Technology: {}".format(entry.technology))
                    imgui.text("Power generaion: {} MW".format(entry.power_generation))
                    imgui.text("Power efficiency: {}%".format(100 * entry.power_efficiency))
                    imgui.text("Heat efficiency: {}%".format(100 * entry.heat_efficiency))
                    imgui.text("Cost of operation: ${}/MWh".format(entry.cost_of_operation))
                    imgui.text("Fail rate: {}%".format(100 * entry.fail_rate))
                    self.__draw_build_tooltip_footer(entry)
            imgui.tree_pop()

        if imgui.tree_node("Power Plant General Buildings"):
            for entry in self.tile_db.get_iter_by_category(ECategory.POWER_PLANT_GENERIC_ELEMENT):
                self.__draw_build_selector_tile(entry, width)
                if imgui.is_item_hovered():
                    self.__draw_build_tooltip_header(entry)
                    imgui.text("Technology: {}".format(entry.technology))
                    imgui.text("{} : {}".format(entry.property_name.replace("_", " ").capitalize(), entry.property_value))
                    self.__draw_build_tooltip_footer(entry)
            imgui.tree_pop()

        if imgui.tree_node("Transmission Lines"):
            for entry in self.tile_db.get_iter_by_category(ECategory.TRANSMISSION_LINE):
                self.__draw_build_selector_tile(entry, width)
                if imgui.is_item_hovered():
                    self.__draw_build_tooltip_header(entry)
                    imgui.text("Proper admittance : {}".format(entry.proper_admittance))
                    imgui.text("Max length : {}".format(entry.max_length))
                    self.__draw_build_tooltip_footer(entry)
            imgui.tree_pop()

        if imgui.tree_node("Other Buildings"):
            for entry in self.tile_db.get_iter_by_category(ECategory.BUILDABLE_OBJECT):
                self.__draw_build_selector_tile(entry, width)
                if imgui.is_item_hovered():
                    self.__draw_build_tooltip_header(entry)
                    self.__draw_build_tooltip_footer(entry)
            imgui.tree_pop()

        if self.selected_category == ECategory.TRANSMISSION_LINE:
            self.game_state = StateSplineBuildMode(self.world, self.view)
            self.__draw_not_implemented()
        elif self.selected != None:
            self.game_state = StateNormalBuildMode(self.world, self.view)

        if not window_open:
            self.gui_state = GUIState.NORMAL
            self.game_state = StateSession(self.world, self.view)

        imgui.end()

    def __draw_build_tooltip_header(self, entry : TileObjectBuildable):
        imgui.begin_tooltip()
        imgui.text(entry.display_name)
        imgui.separator()
        imgui.text("Cost: ${}".format(entry.default_cost))

    def __draw_build_tooltip_footer(self, entry : TileObjectBuildable):
        imgui.separator()
        imgui.text_wrapped(entry.description)
        imgui.end_tooltip()

    def __draw_build_selector_tile(self, entry : TileObjectBase, width : int):
        coord = entry.tileset_coord
        # TODO calculate UV coordinates based in tileset coord
        imgui.image(0, 64, 64, (0.0, 0.0), (0.125, 0.125))
        imgui.same_line()
        if imgui.selectable(entry.display_name, self.selected == entry.name, width = width - 64, height = 64)[1]:
            self.world.last_suggested_object = self.tile_db.get_tileobject_instance(entry.name)
            self.selected = entry.name
            self.selected_category = entry.category

    def __draw_exit_menu(self):
        imgui.open_popup("Do you really want to exit?")
        center_x = self.io.display_size[0]/2
        center_y = self.io.display_size[1]/2

        imgui.set_next_window_position(center_x, center_y, imgui.APPEARING, 0.5, 0.5)

        if imgui.begin_popup_modal("Do you really want to exit?", None, imgui.WINDOW_ALWAYS_AUTO_RESIZE):

            if imgui.button("Exit to desktop", width=170, height=40):
                pygame.event.post(pygame.event.Event(pygame.QUIT))
                imgui.close_current_popup()

            if imgui.button("Resume", width=170, height=40):
                self.gui_state = GUIState.NORMAL
                self.game_state = StateSession(self.world, self.view)
                imgui.close_current_popup()

            imgui.end_popup()

    def __draw_manage_menu(self):
        # TODO
        self.__draw_not_implemented()

    def __draw_not_implemented(self):
        imgui.begin("Work in progress")
        imgui.text("Not implemented yet...")
        if imgui.button("Ok"):
            self.gui_state = GUIState.NORMAL
            self.game_state = StateSession(self.world, self.view)
        imgui.end()

    def __draw_status_bar(self):
        screen_width = self.io.display_size[0]
        # date_dict = self.world.get_current_game_time()
        # date_text = "{}-{}-{}".format(date_dict["day"], date_dict["month"], date_dict["year"])
        # date_text_width = imgui.calc_text_size(date_text)[0]
        
        imgui.set_next_window_position(0.0, 0.0)
        imgui.set_next_window_size(screen_width, 35)
        imgui.push_style_var(imgui.STYLE_ALPHA, 0.7)
        imgui.begin("Status bar", False, imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_SCROLLBAR)
        imgui.text("Bank: ${}".format(self.world.get_current_player_money()))
        # imgui.same_line()
        # imgui.set_cursor_pos_x(screen_width - date_text_width - 10)
        # imgui.text(date_text)
        imgui.pop_style_var(1)
        imgui.end()
        
    def __init__style(self):
        self.style.frame_rounding = 6
        self.style.child_rounding = 6
        self.style.window_rounding = 6
        self.style.popup_rounding = 6

    def render(self):
        imgui.render()
        imgui.end_frame()
        self.impl.render(imgui.get_draw_data())

    @property
    def current_size(self):
        io = imgui.get_io()
        return io.display_size
    
    def want_mouse_capture(self):
        io = imgui.get_io()
        return io.want_capture_mouse
    
    def get_state(self):
        return self.game_state
