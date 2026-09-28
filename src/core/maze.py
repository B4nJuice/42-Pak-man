from mazegenerator import MazeGenerator

from ..utils import Direction, Pos
from .tile import Tile


class Maze:
    _seed: int
    _grid: list[list[Tile]]

    def __init__(self, seed: int) -> None:
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
                self._grid[y].append(Tile(walls=col, x=x, y=y))

    def get_grid(self) -> list[list[Tile]]:
        return self._grid

    def get_tile(self, x: int, y: int) -> Tile:
        return self._grid[y][x]

    def get_next_tile(self, tile: Tile, direction: Direction) -> Tile | None:
        x: int = tile.get_x() + direction.vector[0]
        y: int = tile.get_y() + direction.vector[1]
        if not self.is_within_bounds((x, y)):
            return None

        return self._grid[y][x]

    def is_within_bounds(self, pos: Pos) -> bool:
        return all([
            0 <= pos[0] < self.get_width(),
            0 <= pos[1] < self.get_height()
        ])

    def get_width(self) -> int:
        return len(self._grid[0])

    def get_height(self) -> int:
        return len(self._grid)

    def set_seed(self, seed: int) -> None:
        self._seed = seed

    def get_seed(self) -> int:
        return self._seed

    def print_grid(self) -> None:
        for _, row in enumerate(self._grid):
            top = ''

            for tile in row:
                top += '┌───' if tile.has_wall(Direction.NORTH) else '┌   '

            top += '┐'
            print(top)

            middle = ''
            for tile in row:
                middle += '│   ' if tile.has_wall(Direction.WEST) else '    '

            middle += '│' if row[-1].has_wall(Direction.EAST) else ' '
            print(middle)

        print(
            '└'
            + '───' * (len(self._grid[0]))
            + '─' * (len(self._grid[0]) - 1)
            + '┘'
        )
