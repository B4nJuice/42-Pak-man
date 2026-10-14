from collections.abc import Callable
from typing import Any

from ..color import Color, OperationEnum
from ..mesh import Mesh
from ..position import Position


class Plane(Mesh):
    positions: tuple[Position, Position]
    _on_click: Callable | None

    def __init__(
                self,
                color: Color,
                positions: tuple[Position, Position],
                operation: OperationEnum = OperationEnum.SET,
                dynamic: bool = False,
                on_click: Callable | None = None
            ) -> None:
        super().__init__(
                color,
                operation,
                dynamic
            )

        self.positions = positions
        self._on_click = on_click

    def get_positions(self) -> tuple[Position, Position]:
        return self.positions

    def click(self, x: int, y: int, *args: Any, **kwargs: Any) -> Any:
        if self._on_click and self.contains(x, y):
            self._on_click(*args, **kwargs)

    def contains(self, x: int, y: int) -> bool:
        if self.is_hidden():
            return False
        first, second = self.get_positions()

        return (
            min(first.x, second.x) <= x <= max(first.x, second.x)
            and min(first.y, second.y) <= y <= max(first.y, second.y)
        )
