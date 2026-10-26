import pygame

from src.errors import BaseError
from src.fonts.font_manager import FontManager
from src.game.game import Game
from src.texture.texture_loader import TextureLoader
from src.texture.texture_manager import TextureManager
from src.utils.size import SizeCore

from .app import App
from .config.config_manager import ConfigManager
from .graphics.screen import Screen
from .utils import Logger, TColor


def init_pygame() -> None:
    pygame.init()

    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(
        pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE
    )
    pygame.display.gl_set_attribute(
        pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True
    )


def main(verbose: bool, logger: Logger) -> None:
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

    sizes: SizeCore = SizeCore(
        config.get_config().screen_width,
        config.get_config().screen_height
    )

    texture_manager: TextureManager = TextureManager(
        TextureLoader(screen.moderngl_context),
        default_path='assets/textures'
    )

    fonts: FontManager = FontManager(
        sizes,
        texture_manager,
        screen.moderngl_context
    )

    app: App = App(
        config=config,
        ctx=screen.moderngl_context,
        texture=texture_manager,
        size=sizes,
        fonts=fonts
    )

    game: Game = Game(config.get_config(), screen, app)

    game.run()


if __name__ == '__main__':
    verbose: bool = True

    logger: Logger = Logger(verbose=verbose, name='Main', color=TColor.MAGENTA)
    try:
        main(verbose, logger)
    except BaseError as e:
        logger.error(str(e))
