from mazegenerator import MazeGenerator

from ..utils import Direction
from .cell import Cell


class Level:
    _level: int
    _seed: int
    _grid: list[list[Cell]]

    def __init__(self, seed: int):
        self.set_seed(seed)

    def generate(self, width: int, height: int) -> None:
        self._grid = []
        generator: MazeGenerator = MazeGenerator(
            size=(width, height),
            perfect=False,
            seed=self._seed
        )
        generator.generate()
        for y, row in enumerate(generator.maze):
            self._grid.append([])
            for x, col in enumerate(row):
                self._grid[y].append(Cell(walls=col, x=x, y=y))

    def get_grid(self) -> list[list[Cell]]:
        return self._grid

    def get_cell(self, x: int, y: int) -> Cell:
        return self._grid[y][x]

    def get_width(self) -> int:
        return len(self._grid[0])

    def get_height(self) -> int:
        return len(self._grid)

    def set_seed(self, seed: int):
        self._seed = seed

    def get_seed(self) -> int:
        return self._seed

    def print_level(self) -> None:
        for _, row in enumerate(self._grid):
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

        print(
            '└'
            + '───' * (len(self._grid[0]))
            + '─' * (len(self._grid[0]) - 1)
            + '┘'
        )
