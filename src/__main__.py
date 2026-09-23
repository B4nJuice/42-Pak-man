from .graphics import Screen, Position, Color, OperationEnum
from src.graphics.meshes import Plane, Polygon, ImageTexture, Circle
from src.graphics.super_meshes import Rectangle, MeshLevel

import random
import pygame
from .config import ConfigManager
from .core import Game
from .utils import Color as LoggerColor, Logger


def main(verbose: bool) -> None:
    logger: Logger = Logger(verbose=verbose, name='Main', color=LoggerColor.MAGENTA)
    config: ConfigManager = ConfigManager('config.jsonc', verbose)
    Game(config.get_config())

    config.display_config()

    # game.show_level()
    logger.log('Hello from pak-man!')

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

    game_rectangle = Rectangle(
        Color(255, 255 ,255),
        Position(int(width * 0.25), 100),
        int(width * 0.75 - 100),
        height - 200,
        15
    )

    stats_rectangle = Rectangle(
        Color(255, 255 ,255),
        Position(100, 100),
        int(width * 0.25 - 150),
        height - 200,
        15
    )

    verbose=False

    logger: Logger = Logger(verbose=verbose, name='Main', color=LoggerColor.MAGENTA)
    config: ConfigManager = ConfigManager('config.jsonc', verbose)
    game: Game = Game(config.get_config())

    level: MeshLevel = MeshLevel(
        game._level,
        Color(255, 255, 255),
        Position(int(width * 0.25) + 50, 150),
        height - 300,
        height - 300,
        wall_thickness = 10,
    )

    screen.add_mesh(background)
    screen.add_mesh(game_rectangle)
    screen.add_mesh(stats_rectangle)
    screen.add_mesh(level)
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
