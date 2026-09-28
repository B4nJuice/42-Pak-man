from src.graphics import Mesh, Position, Color, OperationEnum

class Polygon(Mesh):
    def __init__(
                self,
                color: Color,
                positions: list[Position],
                operation: OperationEnum = OperationEnum.SET,
                thickness: int = 1,
                is_dynamic: bool = False,
                smooth_end: bool = False
            ) -> None:
        super().__init__(
                color,
                operation,
                is_dynamic
            )

        self.positions: list[Position] = positions
        self.thickness: int = thickness
        self.smooth_end: bool = smooth_end