from enum import Enum
from typing import Any

from src.graphics import ColorOperations


class OperationEnum(Enum):
    SET = 0
    ADD = 1
    SUBTRACT = 2
    MULTIPLY = 3
    DIVIDE = 4
    MINIMUM = 5
    MAXIMUM = 6
    AVERAGE = 7
    SCREEN = 8
    DIFFERENCE = 9
    INVERT = 10
    ALPHA = 11


class Color:
    def __init__(
                self,
                r: int,
                g: int,
                b: int,
                a: int = 255,
                default: bool = False
            ) -> None:
        self.r: int = self._min_max(r)
        self.g: int = self._min_max(g)
        self.b: int = self._min_max(b)

        self.a: int = self._min_max(a)
        self.is_default: bool = default

    @staticmethod
    def _min_max(
                value: int,
                _min: int = 0,
                _max: int = 255
            ) -> int:
        return (min(_max, max(_min, value)))

    @classmethod
    def default(cls) -> 'Color':
        return Color(0, 0, 0, 255, True)

    @property
    def to_tuple(self) -> tuple[int, int, int, int]:
        return (self.r, self.g, self.b, self.a)
    
    @property
    def to_32(self) -> int:
        return ((self.r << 16) | (self.g << 8) | self.b)

    def apply_operation(
                self,
                color: 'Color',
                operation: OperationEnum,
                **kwargs: Any
            ) -> 'Color':
        return Color(*operation(self, color, **kwargs))