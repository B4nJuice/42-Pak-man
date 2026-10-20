import pygame

from src.texture import TextureLoader

from .app import App, TextureManager
from .config import ConfigManager
from .game import Game
from .graphics import Screen
from .utils import Logger, TColor


def init_pygame():
    pygame.init()

    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(
        pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE
    )
    pygame.display.gl_set_attribute(
        pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True
    )


def main(verbose: bool) -> None:
    logger: Logger = Logger(verbose=verbose, name='Main', color=TColor.MAGENTA)
    logger.log('Starting Pak-man')

    config: ConfigManager = ConfigManager('config.jsonc', verbose)
    # config.display_config()

    init_pygame()

    pygame_screen = pygame.display.set_mode(
        (
            config.get_config().screen_width,
            config.get_config().screen_height,
        ),
        pygame.OPENGL | pygame.DOUBLEBUF  # | pygame.FULLSCREEN,
    )

    pygame.display.set_caption("Pak-man")

    screen: Screen = Screen(
        config.get_config().screen_width,
        config.get_config().screen_height,
        pygame_screen,
    )

    app: App = App(
        config=config,
        ctx=screen.moderngl_context,
        texture=TextureManager(
            TextureLoader(screen.moderngl_context),
            default_path='assets/textures'
        )
    )

    game: Game = Game(config.get_config(), screen, app)

    game.run()


if __name__ == '__main__':
    main(verbose=True)
    # pack = TexturePack.from_directory('assets/textures')
