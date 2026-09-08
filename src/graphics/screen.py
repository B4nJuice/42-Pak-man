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
    
    def add_screen(
                self,
                screen: 'Screen',
                operation: OperationEnum,
                skip_default: bool = True
            ) -> None:
        for y in range(min(self.height, screen.height)):
            for x in range(min(self.width, screen.width)):
                pos: Position = Position(x, y)
                if skip_default:
                    if screen.grid[y][x].default:
                        continue
                    if self.grid[y][x].default:
                        self.put_pixel(
                                position,
                                screen.grid[y][x],
                                OperationEnum.SET
                            )
                    continue
                self.put_pixel(position, screen.grid[y][x], operation)