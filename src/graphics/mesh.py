from collections.abc import Callable

from src.graphics import Color, OperationEnum


class Mesh:
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
