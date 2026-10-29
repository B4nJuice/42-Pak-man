from abc import ABC

from src.graphics.color import Color, OperationEnum


class Mesh(ABC):
    _color: Color
    _operation: OperationEnum
    _hidden: bool

    def __init__(
                self,
                color: Color,
                operation: OperationEnum = OperationEnum.SET
            ) -> None:
        self._color = color
        self._operation = operation
        self._hidden = False

    def get_color(self) -> Color:
        return self._color

    def get_operation(self) -> OperationEnum:
        return self._operation

    def is_hidden(self) -> bool:
        return self._hidden

    def set_color(self, color: Color) -> None:
        self._color = color

    def set_operation(self, operation: OperationEnum) -> None:
        self._operation = operation

    def set_hidden(self, hidden: bool) -> None:
        self._hidden = hidden
