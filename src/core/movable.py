from typing import Any

from ..utils import Direction, Vec2, lerp
from .entity import Entity
from .tile import Tile


class Movable:
    _speed: float
    _target: Tile | None
    _direction: Direction | None
    _progress: float
    _queued: Direction | None
    tile: Tile
    _freeze: bool

    def __init__(self, *args: Any, speed: float = 4.0, **kwargs: Any) -> None:
        """
        Initialize the instance.

        Args:
            speed: Speed used by the operation.
            args: Command-line arguments passed to the application.
            kwargs: Kwargs used by the operation.
        """
        super().__init__(*args, **kwargs)

        if not isinstance(self, Entity):
            raise TypeError('Movable must be used with Entity')

        self.set_speed(speed)
        self._target = None
        self._progress = 0.0
        self._queued = None
        self._direction = None

        self._freeze = False

    def get_speed(self) -> float:
        """
        Return the current speed.

        Returns:
            The current speed.
        """
        return self._speed

    def set_speed(self, speed: float) -> None:
        """
        Assign the speed.

        Args:
            speed: Speed used by the operation.
        """
        self._speed = speed

    def is_moving(self) -> bool:
        """
        Check whether the moving condition holds.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        return self._target is not None or self._freeze

    def get_target(self) -> Tile | None:
        """
        Return the current target.

        Returns:
            The current target.
        """
        return self._target

    def get_direction(self) -> Direction | None:
        """
        Return the current direction.

        Returns:
            The current direction.
        """
        return self._direction

    def set_freeze(self, status: bool) -> None:
        """
        Assign the freeze.

        Args:
            status: New state to assign to the object.
        """
        self._freeze = status

    def toggle_freeze(self) -> None:
        """
        Handle toggle freeze.
        """
        self._freeze = not self._freeze

    def is_frezzed(self) -> bool:
        """
        Check whether the frezzed condition holds.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        return self._freeze

    @property
    def pos(self) -> Vec2:
        """
        Handle pos.

        Returns:
            The value produced by the pos operation.
        """
        if not isinstance(self, Entity):
            return 0.0, 0.0

        if self._target is None:
            return self.get_tile().get_vec()

        p: float = self._progress
        return (
            lerp(self.get_tile().get_x(), self._target.get_x(), p),
            lerp(self.get_tile().get_y(), self._target.get_y(), p)
        )

    def get_target_tile(self) -> Tile:
        """
        Return the current target tile.

        Returns:
            The current target tile.
        """
        if self._target:
            return self._target
        return self.tile

    def try_move(self, direction: Direction, force: bool = False) -> bool:
        """
        Handle try move.

        Args:
            direction: Direction in which the entity should move.
            force: Whether to bypass the usual movement restrictions.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        if not isinstance(self, Entity):
            raise TypeError('Entity does not have a pos property')

        if self._target and self._direction == direction:
            return False

        if self._target is not None:
            if direction.opposite() == self._direction:
                temp = self.get_tile()
                self.tile = self._target
                self._target = temp
                self._direction = direction
                self._progress = 1 - self._progress
                return True
            self._queued = direction
            return False

        next_tile = self.level.get_next_tile(self.get_tile(), direction)
        if next_tile is None:
            return False
        if next_tile.has_wall(direction.opposite()) and not force:
            return False

        self._target = next_tile
        self._direction = direction
        self._progress = 0
        return True

    def try_move_forward(self, force: bool = False) -> bool:
        """
        Handle try move forward.

        Args:
            force: Whether to bypass the usual movement restrictions.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        if self._direction is None:
            return False

        if not isinstance(self, Entity):
            raise TypeError(f'Entity {self}, need to have Entity class !')

        if self._target is not None:
            return False

        next_tile = self.level.get_next_tile(self.get_tile(), self._direction)
        if next_tile is None:
            return False
        if next_tile.has_wall(self._direction.opposite()) and not force:
            return False

        self._target = next_tile
        self._progress = 0
        return True

    def update(self, dt: float) -> None:
        """
        Handle update.

        Args:
            dt: Elapsed time since the previous update, in seconds.
        """
        if not isinstance(self, Entity) or self._freeze:
            return

        if self._target is None or self._direction is None:
            return

        self._progress += self.get_speed() * dt
        if self._progress >= 1.0:
            self._progress -= 1.0
            self.set_tile(self._target)
            current_target: Tile = self._target
            self._target = None
            self.on_arrive(current_target, self._direction)

    def on_arrive(self, tile: Tile, direction: Direction) -> None:
        """
        Handle the arrive event.

        Args:
            tile: Grid tile occupied by or assigned to the entity.
            direction: Direction in which the entity should move.
        """
        pass
