from typing import Protocol

from ..utils import Direction, Vec2, lerp
from .entity import Entity
from .tile import Tile


class MovableEntityProtocol(Protocol):
    _target: Tile | None
    _speed: float
    _progress: float

    def get_tile(self) -> Tile: ...
    def update(self, dt: float) -> None: ...
    def on_arrive(self, tile: Tile) -> None: ...


class Movable:
    _speed: float
    _target: Tile | None
    _progress: float
    _queued: Direction | None

    def __init__(self, *args, speed: float = 4.0, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        if not isinstance(self, Entity):
             raise TypeError('Movable must be used with Entity')

        self.set_speed(speed)
        self._target = None
        self._progress = 0.0
        self._queued = None

    def get_speed(self) -> float:
        return self._speed

    def set_speed(self, speed: float) -> None:
        self._speed = speed

    def is_moving(self) -> bool:
        return self._target is not None

    def get_target(self) -> Tile | None:
        return self._target

    @property
    def pos(self: MovableEntityProtocol) -> Vec2:
        if self._target is None:
            return self.get_tile().get_vec()

        p: float = self._progress
        return (
            lerp(self.get_tile().get_x(), self._target.get_x(), p),
            lerp(self.get_tile().get_y(), self._target.get_y(), p)
        )

    def try_move(self, direction: Direction) -> bool:
        if not isinstance(self, Entity):
            raise TypeError('Entity does not have a pos property')

        if self._target is not None:
            self._queued = direction
            return False

        next_tile = self.level.get_next_tile(self.get_tile(), direction)
        if next_tile is None:
            return False

        self._target = next_tile
        self._progress = 0.0
        return True

    def update(self: MovableEntityProtocol, dt: float) -> None:
        super().update(dt)

        if self._target is None:
            return

        self._progress += self._speed * dt
        if self._progress >= 1.0:
            self._progress = 0.0
            self.on_arrive(self._target)
            self._target = None

    def on_arrive(self, tile: Tile) -> None:
        pass
