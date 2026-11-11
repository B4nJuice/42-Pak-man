from ..utils import Direction, Pos, Vec2


class Tile:
    _x: int
    _y: int
    _walls: int

    def __init__(self, x: int, y: int, walls: int) -> None:
        """
        Initialize the instance.

        Args:
            x: Horizontal coordinate or value.
            y: Vertical coordinate or value.
            walls: Walls used by the operation.
        """
        self._x = x
        self._y = y
        self._walls = walls

    def get_x(self) -> int:
        """
        Return the current x.

        Returns:
            The current x.
        """
        return self._x

    def get_y(self) -> int:
        """
        Return the current y.

        Returns:
            The current y.
        """
        return self._y

    def get_walls(self) -> int:
        """
        Return the current walls.

        Returns:
            The current walls.
        """
        return self._walls

    def get_pos(self) -> Pos:
        """
        Return the current pos.

        Returns:
            The current pos.
        """
        return self._x, self._y

    def get_vec(self) -> Vec2:
        """
        Return the current vec.

        Returns:
            The current vec.
        """
        return float(self._x), float(self._y)

    def has_wall(self, direction: Direction) -> bool:
        """
        Check whether the  wall condition holds.

        Args:
            direction: Direction in which the entity should move.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        return (self._walls & int(direction.value)) != 0

    @property
    def is_full(self) -> bool:
        """
        Check whether the full condition holds.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        return self.get_walls() == 15

    def __str__(self) -> str:
        """
        Return the string representation.

        Returns:
            The value produced by the str operation.
        """
        return f'{self.get_pos()}'
