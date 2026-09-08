from src.graphics import Position, Color, OperationEnum

from pygame import Surface
import numpy as np


class Screen:
    def __init__(
                self,
                width: int,
                height: int,
                pygame_screen: Surface | None = None
            ) -> None:
        self.width: int = width
        self.height: int = height

        self.grid: list[list[Color]] = [
                [
                    Color.default() for _ in range(width)
                ] for _ in range(height)
            ]

        self.pygame_screen: Surface | None = pygame_screen

    def put_pixel(
                self,
                position: Position,
                color: Color,
                operation: OperationEnum = OperationEnum.SET,
                skip_default: bool = True
            ) -> None:

        if position.x < 0 or position.x >= self.width or\
            position.y < 0 or position.y >= self.height:
            # TODO: LOG WARNING
            return

        if color.default:
            return

        if self.grid[position.y][position.x].default:
            operation = OperationEnum.SET

        new_color: Color = self.grid[position.y][position.x].apply_operation(
                color, operation
            )
        self.grid[position.y][position.x] = new_color

        self.pygame_screen.set_at((position.x, position.y), new_color.to_tuple)

    def put_line(
                self,
                start_position: Position,
                end_position: Position,
                color: Color,
                thickness: int = 1,
                operation: OperationEnum = OperationEnum.SET,
                skip_default: bool = True
            ) -> None:

        if thickness <= 0:
            return

        thickness = (thickness + thickness % 2) // 2

        start = np.array(start_position.to_list)
        end = np.array(end_position.to_list)

        n = np.max(np.abs(end - start)) + 1
        coords = np.linspace(start, end, n)

        for coord in np.floor(coords).astype(int):
            self.put_pixel(Position(*coord), color, operation, skip_default)
        
        if thickness > 1:
            vector = end - start

            perp = np.array([
                -vector[1],
                vector[0]
            ], dtype=float)

            perp /= np.linalg.norm(perp)

            for i in range(-thickness, thickness + 1):
                if thickness == 0:
                    continue
                offset = np.round(perp * i).astype(int)

                start_offset = np.array([0, 0])
                end_offset = np.array(offset)

                n = np.max(np.abs(end_offset - start_offset)) + 1
                offsets = np.linspace(start_offset, end_offset, n)

                for of in np.floor(offsets).astype(int):
                    self.put_line(
                        start_position.copy_and_shift(*of),
                        end_position.copy_and_shift(*of),
                        color,
                        operation=operation,
                        skip_default=skip_default
                    )

                    if abs(of[0]) == abs(of[1]):
                        of[0] = of[0] - 1

                        self.put_line(
                            start_position.copy_and_shift(*of),
                            end_position.copy_and_shift(*of),
                            color,
                            operation=operation,
                            skip_default=skip_default
                        )

    def put_polygon(
                self,
                positions: list[Position],
                color: Color,
                operation: OperationEnum = OperationEnum.SET,
                thickness: int = 1,
                skip_default: bool = True,
            ) -> None:
        positions.append(positions[0])

        for i in range(len(positions) - 1):
            self.put_line(
                positions[i],
                positions[i + 1],
                color,
                operation=operation,
                thickness=thickness,
                skip_default=skip_default
                )

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