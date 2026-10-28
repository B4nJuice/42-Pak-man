from collections.abc import Callable

from ..clickable import Clickable
from ..color import Color, OperationEnum
from ..position import Position


class Plane(Clickable):
    positions: tuple[Position, Position]

    def __init__(
                self,
                color: Color,
                positions: tuple[Position, Position],
                operation: OperationEnum = OperationEnum.SET,
                dynamic: bool = False,
                on_click: Callable | None = None,
                on_hover: Callable | None = None,
            ) -> None:
        super().__init__(
                color=color,
                operation=operation,
                dynamic=dynamic,
                on_click=on_click,
                on_hover=on_hover
            )

        self.positions = positions

    def get_positions(self) -> tuple[Position, Position]:
        return self.positions

    def set_width(self, width: float) -> None:
        pos1, pos2 = self.get_positions()

        self.positions = (pos1, Position(pos1.x + width, pos2.y))

    def contains(self, x: int, y: int) -> bool:
        if self.is_hidden():
            return False
        first, second = self.get_positions()

        return (
            min(first.x, second.x) <= x <= max(first.x, second.x)
            and min(first.y, second.y) <= y <= max(first.y, second.y)
        )
