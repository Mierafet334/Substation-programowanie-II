from src.render.camera import Camera
from src.config import Config

import pygame
from typing import Tuple
from math import floor
from pyglm import glm

WorldCoord = Tuple[int, int, int, int]

class View():
    def __init__(self, size_x : int, size_y : int, world_bounds : Tuple[float, float, float, float]):
        aspect = float(size_x) / float(size_y)
        self.__camera = Camera(aspect, Config.CAMERA_Z_NEAR, Config.CAMERA_Z_FAR, world_bounds)
        self.__wheel_y = 0.0
        self.__size_x = size_x
        self.__size_y = size_y

    @property
    def camera(self) -> Camera:
        return self.__camera
    
    def process_event(self, event : pygame.event, block_mouse : bool = False):
        if event.type == pygame.MOUSEWHEEL and not block_mouse:
            self.__wheel_y -= event.y

            if self.__wheel_y > Config.SCROLL_MAX:
                self.__wheel_y = Config.SCROLL_MAX

            elif self.__wheel_y < Config.SCROLL_MIN:
                self.__wheel_y = Config.SCROLL_MIN

    def update(self, delta : float, block_mouse : bool = False):
        speed_x = 0.0
        speed_y = 0.0

        if pygame.mouse.get_focused() and not block_mouse:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            speed_x +=  float(mouse_x < 0.05 * self.__size_x) - float(mouse_x > 0.95 * self.__size_x) 
            speed_y += -float(mouse_y < 0.10 * self.__size_y) + float(mouse_y > 0.95 * self.__size_y)

        keys = pygame.key.get_pressed()
        speed_x += keys[pygame.K_LEFT] - keys[pygame.K_RIGHT]
        speed_y += keys[pygame.K_DOWN] - keys[pygame.K_UP]

        speed_x *= -Config.CAMERA_SPEED_DEFAULT
        speed_y *= -Config.CAMERA_SPEED_DEFAULT

        self.camera.FOV = Config.FOV_MIN + (Config.FOV_MAX - Config.FOV_MIN) * (self.__wheel_y - Config.SCROLL_MIN) / (Config.SCROLL_MAX - Config.SCROLL_MIN)

        self.camera.translate((speed_x * delta, speed_y * delta))

    def set_size(self, size_x : int, size_y : int):
        self.__size_x = size_x
        self.__size_y = size_y
        self.camera.aspect = size_x / size_y

    def screen_to_world_coords(self, x : int, y : int) -> WorldCoord:
        left, right, top, down = self.__camera.get_current_view_bounds()
        world_x = x / self.__size_x * (right - left) + left
        world_y = y / self.__size_y * (down - top) + top
        region_x = floor(world_x)
        region_y = floor(world_y)
        local_x = world_x - region_x
        local_y = world_y - region_y

        local_x_coord = floor(local_x * Config.REGION_SIZE)
        local_y_coord = floor(local_y * Config.REGION_SIZE)

        return (region_x, region_y, local_x_coord, local_y_coord)