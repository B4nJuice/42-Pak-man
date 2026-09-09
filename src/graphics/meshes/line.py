from src.graphics import Mesh, Position, Color, OperationEnum

class Line(Mesh):
    def __init__(
                self,
                color: Color,
                start_position: Position,
                end_position: Position,
                operation: OperationEnum = OperationEnum.SET,
                thickness: int = 1,
                is_dynamic: bool = False
            ) -> None:
        super().__init__(
                color,
                operation,
                is_dynamic
            )

        self.start_position: Position = start_position
        self.end_position: Position = end_position
        self.thickness: int = thickness