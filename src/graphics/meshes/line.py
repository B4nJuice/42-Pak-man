from src.graphics import Mesh, Position, Color, OperationEnum
from math import hypot

class Line(Mesh):
    def __init__(
                self,
                color: Color,
                start_position: Position,
                end_position: Position,
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

        if smooth_end:
            delta_x: int = end_position.x - start_position.x
            delta_y: int = end_position.y - start_position.y
            length: float = hypot(delta_x, delta_y)

            if length > 0:
                extension: float = thickness / (2 * length)
                start_position = Position(
                    start_position.x - delta_x * extension,
                    start_position.y - delta_y * extension
                )
                end_position = Position(
                    end_position.x + delta_x * extension,
                    end_position.y + delta_y * extension
                )

        self.start_position: Position = start_position
        self.end_position: Position = end_position
        self.thickness: int = thickness