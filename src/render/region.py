from OpenGL.GL import *
from pyglm import glm
import numpy as np
from src.config import Config
from typing import Tuple
from src.render.shader_program import ShaderProgram

class Region():
    def __init__(self, world_pos : Tuple[int, int] = (0, 0), data : np.ndarray = np.zeros((Config.REGION_SIZE, Config.REGION_SIZE), dtype=np.int32)):
        self.vertices = list()
        self.tileset_offsets = data.flatten()
        self.highlights = list()

        self.world_pos = world_pos
        self.view_matrix = glm.translate(glm.mat4(1.0), glm.vec3(self.world_pos[0], self.world_pos[1], -Config.REGION_Z_DEPTH))

        self.__generate_points()
        
        if not self.tileset_offsets.size > 0:
            self.__populate_offsets()

        self.__vao = None
        self.__vbo_pos = None
        self.__vbo_data = None
        self.__vbo_highlights = None
        self.__generate_arrays()

    def __generate_points(self):
        for j in reversed(range(0, Config.REGION_SIZE)):
            y = 1.0 / Config.REGION_SIZE * (j + 0.5) - 0.5
            for i in range(Config.REGION_SIZE):
                x = 1.0 / Config.REGION_SIZE * (i + 0.5) - 0.5
                self.vertices += [x, y, 0.0]
                self.highlights.append([0.0, 0.0, 0.0, 0.0])

        self.vertices = np.array(self.vertices, dtype=np.float32)
        self.highlights = np.array(self.highlights, dtype=np.float32)

    def __populate_offsets(self):
        self.tileset_offsets = np.array(np.zeros((Config.REGION_SIZE * Config.REGION_SIZE, )), dtype=np.int32)

        for i in range(16*16):
            self.tileset_offsets[i] = i % 64

    def __generate_arrays(self):
        self.__vao = glGenVertexArrays(1)
        glBindVertexArray(self.__vao)
        self.__vbo_pos = glGenBuffers(1)
        self.__vbo_data = glGenBuffers(1)
        self.__vbo_highlights = glGenBuffers(1)

        glBindBuffer(GL_ARRAY_BUFFER, self.__vbo_pos)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(0))

        glBindBuffer(GL_ARRAY_BUFFER, self.__vbo_data)
        glBufferData(GL_ARRAY_BUFFER, self.tileset_offsets.nbytes, self.tileset_offsets, GL_DYNAMIC_DRAW)

        glEnableVertexAttribArray(1)
        glVertexAttribIPointer(1, 1, GL_INT, 4, ctypes.c_void_p(0))

        glBindBuffer(GL_ARRAY_BUFFER, self.__vbo_highlights)
        glBufferData(GL_ARRAY_BUFFER, self.highlights.nbytes, self.highlights, GL_STATIC_DRAW)

        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 4, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(0))

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def draw(self, shader : ShaderProgram):
        shader.set_mat4("viewMatrix", self.view_matrix)
        glBindVertexArray(self.__vao)
        glDrawArrays(GL_POINTS, 0, int(len(self.vertices)/3))
        glBindVertexArray(0)

    def set_offsets(self, new_offsets : np.ndarray):
        if new_offsets.shape == (Config.REGION_SIZE * Config.REGION_SIZE,):
            self.tileset_offsets = new_offsets
        elif new_offsets.shape == (Config.REGION_SIZE, Config.REGION_SIZE):
            self.tileset_offsets = new_offsets.flatten()
        else:
            raise Exception("Region: Invalid offsets shape, expected {} or {}, got {}".format((Config.REGION_SIZE * Config.REGION_SIZE,), 
                                                                                              (Config.REGION_SIZE, Config.REGION_SIZE), 
                                                                                              new_offsets.shape))
        
        glBindBuffer(GL_ARRAY_BUFFER, self.__vbo_data)
        glBufferData(GL_ARRAY_BUFFER, self.tileset_offsets.nbytes, self.tileset_offsets, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def set_offset(self, coords : Tuple[int, int], new_offset : int):
        offset = coords[0] + (Config.REGION_SIZE - coords[1] - 1) * Config.REGION_SIZE
        self.tileset_offsets[offset] = new_offset
        glBindBuffer(GL_ARRAY_BUFFER, self.__vbo_data)
        glBufferData(GL_ARRAY_BUFFER, self.tileset_offsets.nbytes, self.tileset_offsets, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def get_offset(self, coords : Tuple[int, int]):
        offset = coords[0] + (Config.REGION_SIZE - coords[1] - 1) * Config.REGION_SIZE
        return self.tileset_offsets[offset]

    def set_highlight(self, coords : Tuple[int, int], color : Tuple[int, int, int, int]):
        offset = coords[0] + (Config.REGION_SIZE - coords[1] - 1) * Config.REGION_SIZE
        self.highlights[offset] = color
        glBindBuffer(GL_ARRAY_BUFFER, self.__vbo_highlights)
        glBufferData(GL_ARRAY_BUFFER, self.highlights.nbytes, self.highlights, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def destroy(self):
        glDeleteVertexArrays(1, (self.__vao, ))
        glDeleteBuffers(1, (self.__vbo_pos, ))
        glDeleteBuffers(1, (self.__vbo_data, ))