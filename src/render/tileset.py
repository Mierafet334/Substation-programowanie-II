from OpenGL.GL import *
import pygame

class Tileset():
    def __init__(self, filepath):
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        image = pygame.image.load(filepath).convert_alpha()
        im_width, im_height = image.get_rect().size
        im_data = pygame.image.tobytes(image, "RGBA")
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, im_width, im_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, im_data)
        glGenerateMipmap(GL_TEXTURE_2D)

    def use(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)

    def destroy(self):
        glDeleteTextures(1, (self.texture, ))