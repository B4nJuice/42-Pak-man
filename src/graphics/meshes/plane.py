from collections.abc import Callable

from ..clickable import Clickable
from ..color import Color, OperationEnum
from ..mesh import Mesh
from ..position import Position


class Plane(Clickable, Mesh):
    positions: tuple[Position, Position]

    def __init__(
                self,
                color: Color,
                positions: tuple[Position, Position],
                operation: OperationEnum = OperationEnum.SET,
                dynamic: bool = False,
                on_click: Callable | None = None
            ) -> None:
        super().__init__(
                color=color,
                operation=operation,
                dynamic=dynamic,
                on_click=on_click
            )

        self.positions = positions

    def get_positions(self) -> tuple[Position, Position]:
        return self.positions

    def contains(self, x: int, y: int) -> bool:
        if self.is_hidden():
            return False
        first, second = self.get_positions()

        return (
            min(first.x, second.x) <= x <= max(first.x, second.x)
            and min(first.y, second.y) <= y <= max(first.y, second.y)
        )
