from .graphics import Screen, Position, Color, OperationEnum
from src.graphics.meshes import Plane, Polygon, ImageTexture, Circle
from src.graphics.super_meshes import Rectangle

import random
import pygame
from .config import ConfigManager

def init_pygame():
    pygame.init()

    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(
        pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE
    )
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)


if __name__ == "__main__":
    config: ConfigManager = ConfigManager('config.jsonc')

    init_pygame()

    clock = pygame.time.Clock()

    width, height = 3840, 2160
    pygame_screen = pygame.display.set_mode(
        (width, height),
        pygame.OPENGL | pygame.DOUBLEBUF | pygame.FULLSCREEN,
    )
    pygame.display.set_caption("Pak-man")
    screen: Screen = Screen(width, height, pygame_screen)

    background = Plane(
        Color(0, 0, 0),
        (Position(0, 0), Position(width, height)),
    )

    game = Rectangle(
        Color(255, 255 ,255),
        Position(int(width * 0.25), 100),
        int(width * 0.75 - 100),
        height - 200,
        15
    )

    stats = Rectangle(
        Color(255, 255 ,255),
        Position(100, 100),
        int(width * 0.25 - 150),
        height - 200,
        15
    )

    circle = Circle(
        Color(255, 255, 255),
        Position(500, 500),
        30,
        thickness=5,
        filled=False,
        is_dynamic=True
    )

    circle2 = Circle(
        Color(255, 255, 0),
        Position(600, 500),
        20,
        thickness=5,
        filled=True,
        is_dynamic=True
    )

    screen.add_mesh(background)
    screen.add_mesh(game)
    screen.add_mesh(stats)
    screen.add_mesh(circle)
    screen.add_mesh(circle2)
    screen.refresh()
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.refresh()
        pygame.display.flip()
        clock.tick(60)

    screen.release()
    pygame.quit()
