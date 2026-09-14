from ..config.config_model import ConfigModel
from ..utils import Direction
from ..core import Cell
from mazegenerator import MazeGenerator



class Game:
    _config: ConfigModel
    _level: list[list[Cell]]

    def __init__(self, config: ConfigModel) -> None:
        self._config = config
        self._generate_level()

    def _generate_level(self) -> None:
        maze = MazeGenerator((self._config.level_width, self._config.level_height), False)

        self._level = []
        for y, row in enumerate(maze.maze):
            self._level.append([])
            for x, cell in enumerate(row):
                self._level[y].append(Cell(x, y, cell))

    def show_level(self) -> None:
        for _, row in enumerate(self._level):
            top = ''

            for cell in row:
                top += '┌───' if cell.has_wall(Direction.NORTH) else '┌   '

            top += '┐'
            print(top)

            middle = ''
            for cell in row:
                middle += '│   ' if cell.has_wall(Direction.WEST) else '    '

            middle += '│' if row[-1].has_wall(Direction.EAST) else ' '
            print(middle)

        print('└' + '───' * (self._config.level_width) + '─' * (self._config.level_width - 1) + '┘')

    def load_level(self, level: list[list[Cell]]) -> None:
        self._level = level
