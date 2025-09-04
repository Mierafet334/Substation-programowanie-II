from OpenGL.GL import *
from pyglm import glm

class ShaderProgram():
    def __init__(self, vertex_path, geometry_path, fragment_path):
        # Open and compile shaders
        with open(vertex_path, 'r') as file:
            vertex_code = file.readlines()

        with open(geometry_path, 'r') as file:
            geometry_code = file.readlines()

        with open(fragment_path, 'r') as file:
            fragment_code = file.readlines()

        # Vertex shader
        vertex = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex, vertex_code)
        glCompileShader(vertex)

        result = glGetShaderiv(vertex, GL_COMPILE_STATUS)
        if not (result):
            print("Vertex shader: error compiling")
            raise RuntimeError(glGetShaderInfoLog(vertex))
        
        # Geometry shader
        geometry = glCreateShader(GL_GEOMETRY_SHADER)
        glShaderSource(geometry, geometry_code)
        glCompileShader(geometry)

        result2 = glGetShaderiv(geometry, GL_COMPILE_STATUS)
        if not (result2):
            print("Geometry shader: error compiling")
            raise RuntimeError(glGetShaderInfoLog(geometry))

        # Fragment shader
        fragment = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment, fragment_code)
        glCompileShader(fragment)

        result3 = glGetShaderiv(fragment, GL_COMPILE_STATUS)
        if not (result3):
            print("Fragment shader: error compiling")
            raise RuntimeError(glGetShaderInfoLog(fragment))

        # Link shader program
        self.ID = glCreateProgram()
        glAttachShader(self.ID, vertex)
        glAttachShader(self.ID, geometry)
        glAttachShader(self.ID, fragment)

        glLinkProgram(self.ID)

        success = glGetProgramiv(self.ID, GL_LINK_STATUS)
        if not success:
            infolog = glGetProgramInfoLog(self.ID)
            print("Shader program: linking failed\n", infolog)

        # Free memory associated with shaders
        glDeleteShader(vertex)
        glDeleteShader(geometry)
        glDeleteShader(fragment)

        # Set texture unit to zero by default (assuming that material uses GL_TEXTURE0)
        self.use()
        self.set_texture(0)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Set initial values of transform matrices.
        unit_matrix = glm.mat4(1.0)
        self.set_mat4("modelMatrix", unit_matrix)
        self.set_mat4("viewMatrix", unit_matrix)
        self.set_mat4("projectionMatrix", unit_matrix)

        self.unbind()

    def set_mat4(self, name, matrix):
        glUniformMatrix4fv(glGetUniformLocation(self.ID, name), 1, GL_FALSE, glm.value_ptr(matrix))

    def set_texture(self, number):
        glUniform1i(glGetUniformLocation(self.ID, "imageTexture"), number)

    def use(self):
        glUseProgram(self.ID)

    def unbind(self):
        glUseProgram(0)

    def destroy(self):
        glDeleteProgram(self.ID)

    def clear_screen(self):
        # Not strictly shader related function, can be moved elsewhere
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT)