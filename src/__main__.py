from .config import ConfigManager
from .utils import Color, Logger

# from .core import Game


def main(verbose: bool) -> None:
    logger: Logger = Logger(verbose=verbose, name='Main', color=Color.MAGENTA)
    config: ConfigManager = ConfigManager('config.jsonc', verbose)
    # game: Game = Game(config.get_config())

    config.display_config()

    # game.show_level()
    logger.log('Hello from pak-man!')


if __name__ == '__main__':
    main(True)
