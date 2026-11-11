import os
import sys

import pygame

from src.config.config_manager import ConfigManager
from src.errors import BaseError
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


def main(args: list[str], verbose: bool, logger: Logger) -> None:
    """
    Handle main.

    Args:
        args: Command-line arguments passed to the application.
        verbose: Whether verbose logging is enabled.
        logger: Logger used to report application messages.
    """
    from src.app import App

    logger.log('Starting Pak-man')

    config_file: str = (
        args[0]
        if len(args) > 0
        else 'config.jsonc'
    )
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
        path='.pak-man/leaderboard.json',
        verbose=verbose
    )

    if not leaderboard.get():
        test_entries: list[tuple[str, int, float, bool]] = [
            ('GHOSTBUSTER', 48620, 600, True),
            ('PELLETKING', 42180, 600, True),
            ('BLINKY', 36840, 600, True),
            ('CHERRYBOMB', 21460, 531, False),
            ('DOT_EATER', 19720, 494, False),
            ('INKEY', 16380, 462, False),
        ]
        for name, score, run_time, victory in test_entries:
            leaderboard.add_run(name, score, run_time, victory)

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
    verbose: bool = False

    logger: Logger = Logger(verbose=verbose, name='Main', color=TColor.MAGENTA)
    try:
        main(sys.argv[1:], verbose, logger)
    except BaseError as e:
        logger.error(str(e))
