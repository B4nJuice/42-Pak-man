from typing import Any

from src.core.entity import Entity
from src.core.movable import Movable
from src.core.tile import Tile
from src.utils import Direction


class AI:
    _next_move: list[Direction]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._next_move = []
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

    def has_next_move(self) -> bool:
        return len(self._next_move) > 0

    def clear_next_moves(self) -> None:
        self._next_move.clear()

    def on_arrive(self, tile: Tile, direction: Direction) -> None:
        if not isinstance(self, Movable):
            return

    def update(self, dt: float) -> None:
        if not isinstance(self, Movable) or not isinstance(self, Entity):
            return

        if not self.is_moving() and not self.move_next():
            self.try_move_forward()

        super().update(dt)

    def move_next(self) -> bool:
        if not isinstance(self, Movable) or not self.has_next_move():
            return False

        self.try_move(self.get_next_move())
        return True

    def on_arrive_ai(self) -> None:
        pass
