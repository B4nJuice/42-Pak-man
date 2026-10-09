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

    def __init__(self, *args: Any, speed: float = 4.0, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        if not isinstance(self, Entity):
            raise TypeError('Movable must be used with Entity')

        self.set_speed(speed)
        self._target = None
        self._progress = 0.0
        self._queued = None
        self._direction = None

    def get_speed(self) -> float:
        return self._speed

    def set_speed(self, speed: float) -> None:
        self._speed = speed

    def is_moving(self) -> bool:
        return self._target is not None

    def get_target(self) -> Tile | None:
        return self._target

    def get_direction(self) -> Direction | None:
        return self._direction

    @property
    def pos(self) -> Vec2:
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
        if self._target:
            return self._target
        return self.tile

    def try_move(self, direction: Direction) -> bool:
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
        if next_tile.has_wall(direction.opposite()):
            return False

        self._target = next_tile
        self._direction = direction
        self._progress = 0
        return True

    def try_move_forward(self) -> bool:
        if self._direction is None:
            return False

        if not isinstance(self, Entity):
            raise TypeError(f'Entity {self}, need to have Entity class !')

        if self._target is not None:
            return False

        next_tile = self.level.get_next_tile(self.get_tile(), self._direction)
        if next_tile is None:
            return False
        if next_tile.has_wall(self._direction.opposite()):
            return False

        self._target = next_tile
        self._progress = 0
        return True


    def update(self, dt: float) -> None:
        if not isinstance(self, Entity):
            return

        if self._target is None or self._direction is None:
            return

        self._progress += self._speed * dt
        if self._progress >= 1.0:
            self._progress = 0.0
            self.set_tile(self._target)
            current_target: Tile = self._target
            self._target = None
            self.on_arrive(current_target, self._direction)

        super().update(dt)

    def on_arrive(self, tile: Tile, direction: Direction) -> None:
        pass
