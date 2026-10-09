from ..color import Color, OperationEnum
from ..mesh import Mesh
from ..position import Position


class Plane(Mesh):
    def __init__(
                self,
                color: Color,
                positions: tuple[Position, Position],
                operation: OperationEnum = OperationEnum.SET,
                dynamic: bool = False
            ) -> None:
        super().__init__(
                color,
                operation,
                dynamic
            )

        self.positions: tuple[Position, Position] = positions

    def get_positions(self) -> tuple[Position, Position]:
        return self.positions