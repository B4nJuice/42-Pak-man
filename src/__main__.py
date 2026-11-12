import os
from argparse import ArgumentParser

import pygame

from src.config.config_manager import ConfigManager
from src.fonts.font_manager import FontManager
from src.game.game import Game
from src.graphics.screen import Screen
from src.leaderboard import LeaderboardCore
from src.settings import KeyManager, SettingsManager
from src.texture.texture_loader import TextureLoader
from src.texture.texture_manager import TextureManager
from src.utils import Logger, TColor
from src.utils.size import SizeCore


def init_pygame() -> None:
    """
    Initialize the associated state.
    """
    os.environ['SDL_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR'] = '0'

    pygame.init()

    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(
        pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE
    )
    pygame.display.gl_set_attribute(
        pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True
    )


def main(
        verbose: bool,
        logger: Logger,
        config_file: str
) -> None:
    """
    Handle main.

    Args:
        args: Command-line arguments passed to the application.
        verbose: Whether verbose logging is enabled.
        logger: Logger used to report application messages.
    """
    from src.app import App

    logger.log('Starting Pak-man')

    config: ConfigManager = ConfigManager(config_file, verbose)

    init_pygame()
    pygame_screen = pygame.display.set_mode(
        (
            config.get_config().screen_width,
            config.get_config().screen_height,
        ),
        pygame.OPENGL | pygame.DOUBLEBUF,
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

    settings: SettingsManager = SettingsManager(
        path='.pak-man/settings.json',
        verbose=verbose
    )

    key_manager: KeyManager = KeyManager(
        settings=settings
    )

    leaderboard: LeaderboardCore = LeaderboardCore(
        path=config.get_config().highscore_path,
        verbose=verbose
    )

    app: App = App(
        config=config,
        ctx=screen.moderngl_context,
        texture=texture_manager,
        size=sizes,
        fonts=fonts,
        settings=settings,
        key_manager=key_manager,
        leaderboard=leaderboard
    )

    game: Game = Game(config.get_config(), screen, app)
    game.run()


if __name__ == '__main__':
    parser = ArgumentParser(
        prog='Pak man',
        description=(
            'A modern take on the 1980 arcade classic, rebuilt from scratch in'
            ' Python with its own GPU renderer. '
        ),
        epilog='Enjoy the game!'
    )
    parser.add_argument(
        'config_file',
        nargs='?',
        default='config.jsonc',
        help='Path to the configuration file (default: config.jsonc)'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()
    logger: Logger = Logger(
        verbose=args.verbose,
        color=TColor.MAGENTA,
        name='Main'
    )
    try:
        main(args.verbose, logger, args.config_file)
    except KeyboardInterrupt:
        logger.info(TColor.ITALIC.value + 'Exiting Pak-man...')
    except BaseException as e:
        logger.error(str(e))
