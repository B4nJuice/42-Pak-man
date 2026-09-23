from src.graphics import Mesh, Position, Color, OperationEnum

class Plane(Mesh):
    def __init__(
                self,
                color: Color,
                positions: tuple[Position, Position],
                operation: OperationEnum = OperationEnum.SET,
                is_dynamic: bool = False
            ) -> None:
        super().__init__(
                color,
                operation,
                is_dynamic
            )

        self.positions: tuple[Position, Position] = positions
