from pyglm import glm
from typing import Tuple
from src.config import Config

class Camera():
    def __init__(self, aspect : float, z_near : float, z_far : float, world_bounds : Tuple[float, float, float, float]):
        self.__projection_matrix = glm.mat4(1.0)
        self.__camera_matrix = glm.mat4(1.0)

        self.__ar = aspect
        self.__z_near = z_near
        self.__z_far = z_far
        self.__max = glm.vec2(world_bounds[1] - 0.5, world_bounds[2] - 0.5)
        self.__min = glm.vec2(world_bounds[0] - 0.5, world_bounds[3] - 0.5)
        self.__angle = glm.radians(Config.CAMERA_DEFAULT_FOV)
        self.__world_bounds = world_bounds
        self.__current_translation = glm.vec2(0.0, 0.0)

    @property
    def aspect(self):
        return self.__ar
    
    @aspect.setter
    def aspect(self, new_value):
        self.__ar = new_value

    @property
    def FOV(self):
        return glm.degrees(self.__angle)
    
    @FOV.setter
    def FOV(self, new_value):
        self.__angle = glm.radians(new_value)

    @property
    def transform_matrix(self):
        self.__projection_matrix = glm.perspective(self.__angle, self.__ar, self.__z_near, self.__z_far)
        return self.__projection_matrix * self.__camera_matrix
    
    def translate(self, vec : Tuple[float, float]):
        vec = glm.vec2(vec)
        result = self.__current_translation + vec

        if result.x <= self.__max.x and result.x >= self.__min.x and result.y <= self.__max.y and result.y >= self.__min.y:
            self.__camera_matrix = glm.translate(self.__camera_matrix, glm.vec3(-vec, 0.0)) # VERY important minus before vec
            self.__current_translation += vec

    def get_current_view_bounds(self) -> Tuple[float, float, float, float]:
        # Returns rectangle of camera view in world units, (0.0, 0.0) is the bottom left corner of region(0,0) and (1.0, 1.0) is the top right corner.
        cx, cy = self.__current_translation

        cx += 0.5
        cy += 0.5

        height = 2 * glm.tan(self.__angle / 2) * Config.REGION_Z_DEPTH
        width = height * self.__ar
        return (cx - width / 2, cx + width / 2, cy + height / 2,  cy - height / 2)