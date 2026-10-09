from ..color import Color, OperationEnum
from ..mesh import Mesh
from ..position import Position


class Circle(Mesh):
    position: Position
    radius: int
    thickness: int
    filled: bool

    def __init__(
                self,
                color: Color,
                position: Position,
                radius: int,
                operation: OperationEnum = OperationEnum.SET,
                thickness: int = 1,
                filled: bool = False,
                dynamic: bool = False
            ) -> None:
        super().__init__(
                color,
                operation,
                dynamic
            )

        self.position = position
        self.radius = max(radius, 0)
        self.thickness = max(thickness, 0)
        self.filled = filled

    def get_position(self) -> Position:
        return self.position
