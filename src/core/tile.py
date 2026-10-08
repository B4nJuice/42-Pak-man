from ..utils import Direction, Pos, Vec2


class Tile:
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

    def get_pos(self) -> Pos:
        return self._x, self._y

    def get_vec(self) -> Vec2:
        return float(self._x), float(self._y)

    def has_wall(self, direction: Direction) -> bool:
        return (self._walls & int(direction.value)) != 0

    def __str__(self) -> str:
        return f'{self.get_pos()}'
