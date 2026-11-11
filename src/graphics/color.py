from enum import Enum


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
    r: int
    g: int
    b: int
    a: int
    is_default: bool

    def __init__(
                self,
                r: int,
                g: int,
                b: int,
                a: int = 255,
                default: bool = False
            ) -> None:
        """
        Initialize the instance.

        Args:
            r: R used by the operation.
            g: G used by the operation.
            b: Second value used in the calculation.
            a: First value used in the calculation.
            default: Default used by the operation.
        """
        self.r = self._min_max(r)
        self.g = self._min_max(g)
        self.b = self._min_max(b)

        self.a = self._min_max(a)
        self.is_default = default

    def set_alpha(self, alpha: int) -> None:
        """
        Assign the alpha.

        Args:
            alpha: Alpha used by the operation.
        """
        self.a = min(255, max(0, alpha))

    @staticmethod
    def _min_max(
                value: int,
                _min: int = 0,
                _max: int = 255
            ) -> int:
        """
        Handle min max.

        Args:
            value: Value to assign or apply.
            _min: Min used by the operation.
            _max: Max used by the operation.

        Returns:
            The value produced by the min max operation.
        """
        return (min(_max, max(_min, value)))

    @classmethod
    def default(cls) -> 'Color':
        """
        Handle default.

        Returns:
            The value produced by the default operation.
        """
        return Color(0, 0, 0, 255, True)

    @property
    def to_tuple(self) -> tuple[int, int, int, int]:
        """
        Handle to tuple.

        Returns:
            The value produced by the to tuple operation.
        """
        return (self.r, self.g, self.b, self.a)

    @property
    def to_32(self) -> int:
        """
        Handle to 32.

        Returns:
            The value produced by the to 32 operation.
        """
        return ((self.r << 16) | (self.g << 8) | self.b)
