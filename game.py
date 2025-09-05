from OpenGL.GL import *
import pygame
import sys

from src.render.shader_program import ShaderProgram
from src.render.tileset import Tileset
from src.gui.gui import GUI
from src.render.view import View
from src.saves.world_manager import WorldManager
from src.gameobjects.tile_object_db import TileObjectDB
from src.gamestates import *
from src.config import Config

from pathlib import Path

class Game():
    def __init__(self):
        pygame.init()
        self.size = 800, 600

        pygame.display.set_mode(self.size, pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)
        pygame.display.set_caption("Substation")

        self.world = WorldManager.from_map_file(Path("./resources/test_map.json"))
        self.tile_db = TileObjectDB(Path("./src/tiles_db.json"))

        self.clock = pygame.time.Clock()
        self.view = View(self.size[0], self.size[1], self.world.get_world_bounds())
        self.state = StateSession(self.world, self.view) # Start game in normal session
        self.gui = GUI(self.size[0], self.size[1], self.view, self.world, self.state, self.tile_db)

        self.delta = 0.0 # Delta time for updates

        # Shader loading and compilation
        self.map_shader = ShaderProgram(Path("./src/shaders/vertex.glsl"), Path("./src/shaders/geometry.glsl"), Path("./src/shaders/fragment.glsl"))
        self.material = Tileset(Path("./src/textures/substation_tileset.png"))

    def run(self):
        while True:
            # Pygame event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                
                self.gui.process_event(event)
                if not self.gui.want_mouse_capture():
                    self.view.process_event(event) # Processing events for map scrolling
                    self.state.process_event(event) # Game state dependent processing of events

            self.gui.process_inputs()

            # Update view according to user input
            self.view.update(self.delta, self.gui.want_mouse_capture())

            # GUI preprocessing (does not draw anything into framebuffer)
            self.gui.draw()
            
            self.map_shader.clear_screen()

            # Get current size and update camera aspect ratio
            x, y = self.gui.current_size
            self.view.set_size(x, y)

            # Map rendering
            self.map_shader.use()
            self.material.use()
            self.map_shader.set_mat4("projectionMatrix", self.view.camera.transform_matrix) # Looks ugly here
            self.world.draw(self.map_shader)
            self.map_shader.unbind()

            self.material.use()
            self.gui.render()

            pygame.display.flip()

            self.state = self.gui.get_state()

            # Wait if FPS >60
            self.delta = self.clock.tick(60)

    def quit(self):
        self.world.destroy()
        self.material.destroy()
        self.map_shader.destroy()
        pygame.quit()
        sys.exit(0) # Seems obsolete but without it OpenGL throws exception after closing

if __name__ == "__main__":
    game = Game()
    game.run()