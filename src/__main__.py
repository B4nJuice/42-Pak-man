from .config import ConfigManager
from .core import Game
from .utils import Color, Logger


def main(verbose: bool) -> None:
    logger: Logger = Logger(verbose=verbose, name='Main', color=Color.MAGENTA)
    config: ConfigManager = ConfigManager('config.jsonc', verbose)
    Game(config.get_config())

    config.display_config()

    # game.show_level()
    logger.log('Hello from pak-man!')


if __name__ == '__main__':
    main(True)
