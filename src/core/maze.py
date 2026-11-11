from random import randint

from mazegenerator import MazeGenerator

from src.config.level_model import LevelModel
from src.errors import MazeGenerationError

from ..utils import Direction, Pos
from .tile import Tile

_DIRECTIONS: tuple[Direction, ...] = tuple(Direction)


class Maze:
    _seed: int
    _grid: list[list[Tile]]
    _moves_cache: dict[Tile, list[tuple[Tile, Direction]]]

    def __init__(self, seed: int) -> None:
        """
        Initialize the instance.

        Args:
            seed: Seed used by the operation.
        """
        self.set_seed(seed)
        self._moves_cache = {}

    def generate(self, level: LevelModel) -> None:
        """
        Handle generate.

        Args:
            level: Level containing the entity or navigation data.
        """
        self.invalidate_moves_cache()
        self._grid = []
        try:
            generator: MazeGenerator = MazeGenerator(
                size=(level.level_width, level.level_height),
                perfect=False,
                seed=self._seed
            )
            maze: list[list[int]] = generator.maze
        except Exception as e:
            raise MazeGenerationError(
                f'Maze generator failed for level {level.name!r} '
                f'({level.level_width}x{level.level_height}, '
                f'seed={self._seed}): {type(e).__name__}: {e}'
            ) from e
        if not maze or not maze[0]:
            raise MazeGenerationError(
                f'Maze generator returned an empty maze for level '
                f'{level.name!r}'
            )
        for y, row in enumerate(maze):
            self._grid.append([])
            for x, col in enumerate(row):
                self._grid[y].append(Tile(walls=col, x=x, y=y))

    def get_grid(self) -> list[list[Tile]]:
        """
        Return the current grid.

        Returns:
            The current grid.
        """
        return self._grid

    def get_tile(self, x: int, y: int) -> Tile:
        """
        Return the current tile.

        Args:
            x: Horizontal coordinate or value.
            y: Vertical coordinate or value.

        Returns:
            The current tile.
        """
        return self._grid[y][x]

    def get_next_tile(self, tile: Tile, direction: Direction) -> Tile | None:
        """
        Return the current next tile.

        Args:
            tile: Grid tile occupied by or assigned to the entity.
            direction: Direction in which the entity should move.

        Returns:
            The current next tile.
        """
        x: int = tile.get_x() + direction.vector[0]
        y: int = tile.get_y() + direction.vector[1]
        if not self.is_within_bounds((x, y)):
            return None

        return self._grid[y][x]

    def get_tile_ahead(
                self,
                tile: Tile,
                direction: Direction,
                distance: int
            ) -> Tile:
        """
        Return the current tile ahead.

        Args:
            tile: Grid tile occupied by or assigned to the entity.
            direction: Direction in which the entity should move.
            distance: Distance used by the operation.

        Returns:
            The current tile ahead.
        """
        x: int = tile.get_x() + direction.vector[0] * distance
        y: int = tile.get_y() + direction.vector[1] * distance

        while not self.is_within_bounds((x, y)):
            distance -= 1
            x = tile.get_x() + direction.vector[0] * distance
            y = tile.get_y() + direction.vector[1] * distance

        return self._grid[y][x]

    def is_within_bounds(self, pos: Pos) -> bool:
        """
        Check whether the within bounds condition holds.

        Args:
            pos: Pos used by the operation.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        return 0 <= pos[0] < self.get_width() \
            and 0 <= pos[1] < self.get_height()

    def get_possible_moves(self, tile: Tile) -> list[tuple[Tile, Direction]]:
        """
        Return the current possible moves.

        Args:
            tile: Grid tile occupied by or assigned to the entity.

        Returns:
            The current possible moves.
        """
        moves = self._moves_cache.get(tile)
        if moves is None:
            moves = self._compute_moves(tile)
            self._moves_cache[tile] = moves
        return moves

    def get_random_tile(self) -> Tile:
        """
        Return the current random tile.

        Returns:
            The current random tile.
        """
        x: int = randint(0, self.get_width() - 1)
        y: int = randint(0, self.get_height() - 1)

        return self.get_tile(x, y)

    def get_random_valid_tile(self) -> Tile:
        """
        Return the current random valid tile.

        Returns:
            The current random valid tile.
        """
        tile: Tile | None = None

        while tile is None:
            tile = self.get_random_tile()
            if tile.is_full:
                tile = None

        return tile

    def _compute_moves(self, tile: Tile) -> list[tuple[Tile, Direction]]:
        """
        Handle compute moves.

        Args:
            tile: Grid tile occupied by or assigned to the entity.

        Returns:
            The value produced by the compute moves operation.
        """
        x0, y0 = tile.get_x(), tile.get_y()
        width, height = self.get_width(), self.get_height()
        moves: list[tuple[Tile, Direction]] = []

        for direction in _DIRECTIONS:
            if tile.has_wall(direction):
                continue
            dx, dy = direction.vector
            x, y = x0 + dx, y0 + dy
            if 0 <= x < width and 0 <= y < height:
                moves.append((self._grid[y][x], direction))

        return moves

    def invalidate_moves_cache(self) -> None:
        """
        Handle invalidate moves cache.
        """
        self._moves_cache.clear()

    def get_width(self) -> int:
        """
        Return the current width.

        Returns:
            The current width.
        """
        return len(self._grid[0])

    def get_height(self) -> int:
        """
        Return the current height.

        Returns:
            The current height.
        """
        return len(self._grid)

    def set_seed(self, seed: int) -> None:
        """
        Assign the seed.

        Args:
            seed: Seed used by the operation.
        """
        self._seed = seed

    def get_seed(self) -> int:
        """
        Return the current seed.

        Returns:
            The current seed.
        """
        return self._seed

    def print_grid(self) -> None:
        """
        Handle print grid.
        """
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
