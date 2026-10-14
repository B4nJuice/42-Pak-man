from collections.abc import Callable
from abc import ABC

from src.graphics import Color, OperationEnum


class Mesh(ABC):
    _color: Color
    _operation: OperationEnum
    _hidden: bool
    _dynamic: bool
    _on_click: Callable | None

    def __init__(
                self,
                color: Color,
                operation: OperationEnum = OperationEnum.SET,
                dynamic: bool = False,
                on_click: Callable | None = None
            ) -> None:
        self._color = color
        self._operation = operation
        self._hidden = False
        self._dynamic = dynamic
        self._on_click = on_click

    def get_color(self) -> Color:
        return self._color

    def get_operation(self) -> OperationEnum:
        return self._operation

    def is_hidden(self) -> bool:
        return self._hidden

    def is_dynamic(self) -> bool:
        return self._dynamic

    def set_color(self, color: Color) -> None:
        self._color = color

    def set_operation(self, operation: OperationEnum) -> None:
        self._operation = operation

    def set_hidden(self, hidden: bool) -> None:
        self._hidden = hidden

    def contains(self, x: float, y: float) -> bool:
        first, second = self.get_positions()

        return (
            min(first.x, second.x) <= x <= max(first.x, second.x)
            and min(first.y, second.y) <= y <= max(first.y, second.y)
        )
