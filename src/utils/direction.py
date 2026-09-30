from enum import Enum

from .types import Pos


class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    @property
    def vector(self) -> Pos:
        return {
            Direction.NORTH: (0, -1),
            Direction.EAST: (1, 0),
            Direction.SOUTH: (0, 1),
            Direction.WEST: (-1, 0),
        }[self]

    def opposite(self) -> 'Direction':
        return {
            Direction.NORTH: Direction.SOUTH,
            Direction.EAST: Direction.WEST,
            Direction.SOUTH: Direction.NORTH,
            Direction.WEST: Direction.EAST,
        }[self]

    def __str__(self) -> str:
        return {
            Direction.NORTH: 'NORTH',
            Direction.EAST: 'EAST',
            Direction.SOUTH: 'SOUTH',
            Direction.WEST: 'WEST',
        }[self]

    def to_string(self) -> str:
        return str(self).lower()
