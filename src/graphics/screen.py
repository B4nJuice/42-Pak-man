from src.graphics import Position, Color, OperationEnum, Mesh
from src.graphics.meshes import Line, Polygon

from functools import singledispatchmethod
from pygame import Surface
import numpy as np
import pygame 


class Layer:
    def __init__(
                self,
                width: int,
                height: int,
                operation: OperationEnum = OperationEnum.SET
            ) -> None:
        self.width: int = width
        self.height: int = height
        self.operation: OperationEnum = operation

        self.grid: list[list[Color]] = np.full(
                (self.height, self.width), Color.default(), dtype=object
            )

        self.dirty_grid: list[list[bool]] = np.zeros(
                (self.height, self.width), dtype=bool
            )

        self.meshes: list[Mesh] = []

    def add_layer(
                self,
                layer: 'Layer',
                skip_default: bool = True
            ) -> None:
        for y in range(min(self.height, layer.height)):
            for x in range(min(self.width, layer.width)):
                pos: Position = Position(x, y)
                if skip_default:
                    if layer.grid[y][x].is_default:
                        continue
                    if self.grid[y][x].is_default:
                        self.put_pixel(
                                pos,
                                layer.grid[y][x],
                                OperationEnum.SET
                            )
                    continue
                self.put_pixel(position, layer.grid[y][x], layer.operation)

    @singledispatchmethod
    def put_mesh(
                self,
                mesh: Mesh,
                skip_default: bool = True
            ) -> None:
        print(mesh)

    @put_mesh.register(Line)
    def put_line(
                self,
                line: Line,
                skip_default: bool = True,
                source_mesh: Mesh | None = None
            ) -> None:

        if line.thickness <= 0:
            return

        thickness = (line.thickness + line.thickness % 2) // 2

        start = np.array(line.start_position.to_list)
        end = np.array(line.end_position.to_list)

        n = np.max(np.abs(end - start)) + 1
        coords = np.linspace(start, end, n)

        for coord in np.floor(coords).astype(int):
            if source_mesh:
                source_mesh.clean_pixel.append(coord)
            else:
                line.clean_pixel.append(coord)
            self.put_pixel(
                    Position(*coord),
                    line.color,
                    line.operation,
                    skip_default
                )

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
                        Line(
                            line.color,
                            line.start_position.copy_and_shift(*of),
                            line.end_position.copy_and_shift(*of),
                            operation=line.operation
                        ),
                        skip_default=skip_default,
                        source_mesh=source_mesh or line
                    )

                    if abs(of[0]) == abs(of[1]):
                        of[0] = of[0] - 1

                        self.put_line(
                            Line(
                                line.color,
                                line.start_position.copy_and_shift(*of),
                                line.end_position.copy_and_shift(*of),
                                operation=line.operation
                            ),
                            skip_default=skip_default,
                            source_mesh=source_mesh or line
                        )

    @put_mesh.register(Polygon)
    def put_polygon(
                self,
                polygon: Polygon,
                skip_default: bool = True,
            ) -> None:
        polygon.positions.append(polygon.positions[0])

        for i in range(len(polygon.positions) - 1):
            self.put_line(
                    Line(
                        polygon.color,
                        polygon.positions[i],
                        polygon.positions[i + 1],
                        operation=polygon.operation,
                        thickness=polygon.thickness,
                    ),
                    source_mesh=polygon
                )

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

        if color.is_default:
            return

        if self.grid[position.y][position.x].is_default:
            operation = OperationEnum.SET

        new_color: Color = self.grid[position.y][position.x].apply_operation(
                color,
                operation
            )
        self.grid[position.y][position.x] = new_color

    def refresh_grid(
                self
            ) -> None:
        for mesh in self.meshes:
            self.put_mesh(
                    mesh
                )


class Screen:
    def __init__(
                self,
                width: int,
                height: int,
                pygame_screen: Surface
            ) -> None:
        self.width: int = width
        self.height: int = height

        self.grid: Layer = Layer(self.width, self.height)

        self.static_mesh_layer: Layer = Layer(
                width,
                height
            )
        self.dynamic_mesh_layer: Layer = Layer(
                width,
                height
            )

        self.pygame_screen: Surface = pygame_screen
        self.pygame_matrix: list[int] = pygame.surfarray.pixels2d(
                self.pygame_screen
            )

    def add_mesh(
                self,
                mesh: Mesh
            ) -> None:
        if mesh.is_dynamic:
            self.dynamic_mesh_layer.meshes.append(mesh)
        else:
            self.static_mesh_layer.meshes.append(mesh)

    def put_pixel(
                self,
                position: Position,
                color: Color
            ) -> None:
        self.pygame_matrix[position.x][position.y] = color.to_32

    def init(
                self
            ) -> None:
        self.static_mesh_layer.refresh_grid()
        self.dynamic_mesh_layer.refresh_grid()
        self.grid.add_layer(self.static_mesh_layer)
        self.grid.add_layer(self.dynamic_mesh_layer)
        for y in range(self.height):
            for x in range(self.width):
                self.put_pixel(Position(x, y), self.grid.grid[y][x])

    def clear_at(
                self,
                positions: list[list[int]]
            ) -> None:
        for position in positions:
            x, y = position
            self.pygame_matrix[x][y] =\
                self.static_mesh_layer.grid[y][x].to_32
