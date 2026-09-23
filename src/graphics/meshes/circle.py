from src.graphics import Mesh, Position, Color, OperationEnum

class Circle(Mesh):
    def __init__(
                self,
                color: Color,
                position: Position,
                radius: int,
                operation: OperationEnum = OperationEnum.SET,
                thickness: int = 1,
                filled: bool = False,
                is_dynamic: bool = False
            ) -> None:
        super().__init__(
                color,
                operation,
                is_dynamic
            )

        self.position: Position = position
        self.radius: int = max(radius, 0)
        self.thickness: int = max(thickness, 0)
        self.filled: bool = filled
