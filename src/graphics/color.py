from enum import Enum
from typing import Any

from src.graphics import ColorOperations


class OperationEnum(Enum):
    SET = ColorOperations.set_color
    ADD = ColorOperations.add
    SUBTRACT = ColorOperations.subtract
    MULTIPLY = ColorOperations.multiply
    DIVIDE = ColorOperations.divide
    MINIMUM = ColorOperations.minimum
    MAXIMUM = ColorOperations.maximum
    AVERAGE = ColorOperations.average
    SCREEN = ColorOperations.screen
    DIFFERENCE = ColorOperations.difference
    INVERT = ColorOperations.invert
    ALPHA = ColorOperations.alpha


class Color:
    def __init__(
                self,
                r: int,
                g: int,
                b: int,
                a: int = 255
            ) -> None:
        self.r: int = self._min_max(r)
        self.g: int = self._min_max(g)
        self.b: int = self._min_max(b)

        self.a: int = self._min_max(a)

    @staticmethod
    def _min_max(
                value: int,
                _min: int = 0,
                _max: int = 255
            ) -> int:
        return (min(_max, max(_min, value)))

    @classmethod
    @property
    def default(cls) -> 'Color':
        return Color(0, 0, 0, 255)

    def apply_operation(
                self,
                color: 'Color',
                operation: OperationEnum,
                *kwargs: Any
            ) -> 'Color':
        return operation.value()(self, color, **kwargs)