from ..utils import Direction


class Cell:
    _x: int
    _y: int
    _walls: int

    def __init__(self, x: int, y: int, walls: int) -> None:
        self._x = x
        self._y = y
        self._walls = walls

    def get_x(self) -> int:
        return self._x

    def get_y(self) -> int:
        return self._y

    def get_walls(self) -> int:
        return self._walls

    def has_wall(self, direction: Direction) -> bool:
        return (self._walls & direction.value) != 0

    def __str__(self) -> str:
        n = self.has_wall(Direction.NORTH)
        e = self.has_wall(Direction.EAST)
        s = self.has_wall(Direction.SOUTH)
        w = self.has_wall(Direction.WEST)

        chars = {
            (False, False, False, False): " ",
            (True,  False, False, False): "╵",
            (False, True,  False, False): "╴",
            (False, False, True,  False): "╷",
            (False, False, False, True ): "╶",

            (True,  True,  False, False): "└",
            (True,  False, True,  False): "│",
            (True,  False, False, True ): "┘",
            (False, True,  True,  False): "┌",
            (False, True,  False, True ): "─",
            (False, False, True,  True ): "┐",

            (True, True, True, False): "├",
            (True, True, False, True): "┴",
            (True, False, True, True): "┤",
            (False, True, True, True): "┬",

            (True, True, True, True): "┼",
        }

        return chars[(n, e, s, w)]
