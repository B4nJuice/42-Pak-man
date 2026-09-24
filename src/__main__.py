from .graphics import Screen, Position, Color, OperationEnum
from src.graphics.meshes import Plane, Polygon, ImageTexture, Circle
from src.graphics.super_meshes import Bar, Rectangle, MeshLevel, FontSequence
from src.graphics.font import Font

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
        Position(int(width * 0.25), 250),
        int(width * 0.75 - 100),
        height - 350,
        15,
        smooth_end=True
    )

    stats_rectangle = Rectangle(
        Color(255, 255 ,255),
        Position(100, 100),
        int(width * 0.25 - 150),
        height - 200,
        15,
        smooth_end=True
    )

    verbose=False

    logger: Logger = Logger(verbose=verbose, name='Main', color=LoggerColor.MAGENTA)
    config: ConfigManager = ConfigManager('config.jsonc', verbose)
    game: Game = Game(config.get_config())

    level: MeshLevel = MeshLevel(
        game._level,
        Color(255, 255, 255),
        Position(int(width * 0.25) + 50, 300),
        min(height - 400, int(width * 0.75) - 150),
        min(height - 400, int(width * 0.75) - 150),
        wall_thickness=10,
        smooth_end=True
    )

    progress_bar: Bar = Bar(
        Color(30, 80, 180),
        Color(255, 255, 255),
        Position(int(width * 0.25) + 100, 150),
        int(width * 0.75) - 300,
        50,
        5,
        goal=100,
        is_dynamic=True,
        smooth_end=True
    )

    font = Font(
            'assets/fonts/Barge-Black.otf',
            screen.moderngl_context,
            pixel_size=48
        )
    progress_text_value = '00%'
    progress_text_width = sum(
        font.characters[character]['advance']
        for character in progress_text_value
    )
    progress_text_height = max(
        font.characters[character]['height']
        for character in progress_text_value
    )
    progress_text_bearing = max(
        font.characters[character]['bearing_y']
        for character in progress_text_value
    )
    progress_text: FontSequence = FontSequence(
        progress_text_value,
        font,
        Color(255, 255, 255),
        Position(
            progress_bar.position.x
            + (progress_bar.width - progress_text_width) // 2,
            progress_bar.position.y
            + (progress_bar.height - progress_text_height) // 2
            + progress_text_bearing,
        ),
        is_dynamic=True,
        spacing=2
    )

    screen.add_mesh(background)
    screen.add_mesh(game_rectangle)
    screen.add_mesh(stats_rectangle)
    screen.add_mesh(progress_bar)
    screen.add_mesh(progress_text)
    screen.add_mesh(level)
    screen.refresh()
    pygame.display.flip()

    running = True
    elapsed = 0.0
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        elapsed = (elapsed + dt) % 4.0
        cycle_progress = elapsed if elapsed <= 2.0 else 4.0 - elapsed
        progress_bar.set_progression(int(cycle_progress / 2.0 * progress_bar.goal))
        progress_text.set_sequence_text(f'{progress_bar.progression:02d}%')

        screen.refresh()
        pygame.display.flip()
