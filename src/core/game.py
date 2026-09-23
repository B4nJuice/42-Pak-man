from ..config import ConfigModel
from .level import Level


class Game:
    _config: ConfigModel
    _level: Level

    def __init__(self, config: ConfigModel) -> None:
        self._config = config
        self._level = Level(0)
        self._level.generate(
            self._config.level_width,
            self._config.level_height
        )

        self._level.print_grid()
