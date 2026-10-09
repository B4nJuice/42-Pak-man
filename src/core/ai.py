from abc import abstractmethod
from typing import Any

from src.core.entity import Entity
from src.core.movable import Movable
from src.core.tile import Tile
from src.utils import Direction


class AI:
    _next_move: list[Direction]
    _tracking_tile: Tile | None
    _elapsed_traking_update: float
    _tile_has_change: bool
    _invalid_tracinkg_time: float | None
    _has_arrive: bool

    def __init__(self, *args: Any, update_tracking_interval: float | None, **kwargs: Any) -> None:
        self._next_move = []

        self._tracking_tile = None
        self._elapsed_traking_update = float('inf')
        self._tile_has_change = False
        self._invalid_tracinkg_time = update_tracking_interval
        self._has_arrive = True

        super().__init__(*args, **kwargs)

    def get_next_move(self) -> Direction:
        return self._next_move.pop(0)

    def set_next_moves(self, next_move: list[Direction]) -> None:
        self._next_move = next_move

    def add_next_move(self, direction: Direction) -> None:
        if not isinstance(self, Movable):
            return

        self._next_move.append(direction)

        if self._direction is None:
            self.move_next()

    def apply_path(self, path: list[tuple[Tile, Direction]]) -> None:
        for _, direction in path:
            self.add_next_move(direction)

    def has_next_move(self) -> bool:
        return len(self._next_move) > 0

    def clear_next_moves(self) -> None:
        self._next_move.clear()

    def move_next(self) -> bool:
        if not isinstance(self, Movable) or not isinstance(self, Entity):
            return False

        if not self.has_next_move():
            if self.get_tile() == self._tracking_tile and not self._has_arrive:
                self._has_arrive = True
                self.on_arrive_ai()
            return False

        self.try_move(self.get_next_move())
        return True

    def on_arrive_ai(self) -> None:
        pass

    def update_ai(self, dt: float) -> None:
        if not isinstance(self, Movable) or not isinstance(self, Entity):
            return

        self.set_tracking_tile(self.get_tracking_tile())

        if self.need_to_update(dt):
            self.update_tracking()

        if not self.is_moving():
            self.move_next()

    def update_tracking(self) -> None:
        self._elapsed_traking_update = 0.0
        self._tile_has_change = False
        self._need_update_tracking = False

    def force_update_tracking(self) -> None:
        self.update_tracking()

    def set_tracking_tile(self, tile: Tile) -> None:
        if self._tracking_tile != tile:
            self._tracking_tile = tile
            self._tile_has_change = True
            self._has_arrive = False

    def need_to_update(self, dt: float) -> bool:
        self._elapsed_traking_update += dt

        return self._tile_has_change and \
        (
            self._invalid_tracinkg_time is None or
            (self._elapsed_traking_update >= self._invalid_tracinkg_time
                or (isinstance(self, Movable) and not self.is_moving())
            )
        )

    @abstractmethod
    def get_tracking_tile(self) -> Tile:
        pass
