from copy import deepcopy


class Position:
    def __init__(
                self,
                x: int,
                y: int
            ) -> None:
        self.x: int = x
        self.y: int = y
    
    @property
    def to_list(self) -> list[int]:
        return [self.x, self.y]

    def copy_and_shift(
                self,
                x_offset: int,
                y_offset: int
            ) -> 'Position':
        new: 'Position' = deepcopy(self)
        new.x += x_offset
        new.y += y_offset

        return new
