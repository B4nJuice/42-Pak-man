from src.graphics import Position, Color, OperationEnum

class Screen:
    def __init__(
                self,
                width: int,
                height: int
            ) -> None:
        self.width: int = width
        self.height: int = height

        self.grid: list[list[Color]] = [
                [
                    Color.default for _ in range(width)
                ] for _ in range(height)
            ]

    def put_pixel(
                self,
                position: Position,
                color: Color,
                operation: OperationEnum
            ) -> None:
        self.grid[position.y][position.x] =\
            Color.apply_operation(color, OperationEnum)