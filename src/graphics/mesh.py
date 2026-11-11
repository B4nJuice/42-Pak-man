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
        """
        Initialize the instance.

        Args:
            color: Color applied to the rendered element.
            operation: Operation used by the operation.
        """
        self._color = color
        self._operation = operation
        self._hidden = False

    def get_color(self) -> Color:
        """
        Return the current color.

        Returns:
            The current color.
        """
        return self._color

    def get_operation(self) -> OperationEnum:
        """
        Return the current operation.

        Returns:
            The current operation.
        """
        return self._operation

    def is_hidden(self) -> bool:
        """
        Check whether the hidden condition holds.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        return self._hidden

    def set_color(self, color: Color) -> None:
        """
        Assign the color.

        Args:
            color: Color applied to the rendered element.
        """
        self._color = color

    def set_operation(self, operation: OperationEnum) -> None:
        """
        Assign the operation.

        Args:
            operation: Operation used by the operation.
        """
        self._operation = operation

    def set_hidden(self, hidden: bool) -> None:
        """
        Assign the hidden.

        Args:
            hidden: Hidden used by the operation.
        """
        self._hidden = hidden
