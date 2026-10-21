from copy import deepcopy


class Position:
    x: float
    y: float

    def __init__(
                self,
                x: float,
                y: float
            ) -> None:
        self.x = x
        self.y = y

    @property
    def to_list(self) -> list[float]:
        return [self.x, self.y]

    def copy_and_shift(
                self,
                x_offset: float,
                y_offset: float
            ) -> 'Position':
        new: Position = deepcopy(self)
        new.x += x_offset
        new.y += y_offset

        return new
