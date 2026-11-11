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
                on_click: Callable | None = None,
                on_hover: Callable | None = None,
            ) -> None:
        """
        Initialize the instance.

        Args:
            color: Color applied to the rendered element.
            positions: Positions used by the operation.
            operation: Operation used by the operation.
            on_click: On click used by the operation.
            on_hover: On hover used by the operation.
        """
        super().__init__(
                color=color,
                operation=operation,
                on_click=on_click,
                on_hover=on_hover
            )

        self.positions = positions

    def get_positions(self) -> tuple[Position, Position]:
        """
        Return the current positions.

        Returns:
            The current positions.
        """
        return self.positions

    def set_width(self, width: float) -> None:
        """
        Assign the width.

        Args:
            width: Width of the screen or rendered element.
        """
        pos1, pos2 = self.get_positions()

        self.positions = (pos1, Position(pos1.x + width, pos2.y))

    def contains(self, x: int, y: int) -> bool:
        """
        Handle contains.

        Args:
            x: Horizontal coordinate or value.
            y: Vertical coordinate or value.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        if self.is_hidden():
            return False
        first, second = self.get_positions()

        return (
            min(first.x, second.x) <= x <= max(first.x, second.x)
            and min(first.y, second.y) <= y <= max(first.y, second.y)
        )
