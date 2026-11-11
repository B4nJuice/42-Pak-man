from copy import deepcopy


class Position:
    x: float
    y: float

    def __init__(
                self,
                x: float,
                y: float
            ) -> None:
        """
        Initialize the instance.

        Args:
            x: Horizontal coordinate or value.
            y: Vertical coordinate or value.
        """
        self.x = x
        self.y = y

    @property
    def to_list(self) -> list[float]:
        """
        Handle to list.

        Returns:
            The value produced by the to list operation.
        """
        return [self.x, self.y]

    def copy_and_shift(
                self,
                x_offset: float,
                y_offset: float
            ) -> 'Position':
        """
        Handle copy and shift.

        Args:
            x_offset: X offset used by the operation.
            y_offset: Y offset used by the operation.

        Returns:
            The value produced by the copy and shift operation.
        """
        new: Position = deepcopy(self)
        new.x += x_offset
        new.y += y_offset

        return new
