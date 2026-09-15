from .config import ConfigManager
from .core import Game

def main():
    config: ConfigManager = ConfigManager('config.jsonc')
    # game: Game = Game(config.get_config())

    config.display_config()

    print("Hello from pak-man!")
    # game.show_level()


if __name__ == "__main__":
    main()
