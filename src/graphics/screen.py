from src.graphics import Position, Color, OperationEnum, Mesh
from src.graphics.meshes import Line, Polygon, Plane

from functools import singledispatchmethod
from pygame import Surface
import numpy as np
import pygame 

from .gpu_renderer import GPURenderer


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
        self.gpu_mode: bool = False

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
                skip_default: bool = True,
                positions: set[tuple[int, int]] | None = None,
                record_pixels: bool = True,
                collected_pixels: set[tuple[int, int]] | None = None
            ) -> None:
        ...

    @put_mesh.register(Line)
    def put_line(
                self,
                line: Line,
                skip_default: bool = True,
                source_mesh: Mesh | None = None,
                positions: set[tuple[int, int]] | None = None,
                record_pixels: bool = True,
                collected_pixels: set[tuple[int, int]] | None = None
            ) -> None:

        if line.thickness <= 0:
            return

        thickness = (line.thickness + line.thickness % 2) // 2

        start = np.array(line.start_position.to_list)
        end = np.array(line.end_position.to_list)

        n = np.max(np.abs(end - start)) + 1
        coords = np.linspace(start, end, n)

        for coord in np.floor(coords).astype(int):
            if record_pixels:
                if positions is None or tuple(coord) in positions:
                    if source_mesh:
                        source_mesh.clean_pixel.append(coord.tolist())
                    else:
                        line.clean_pixel.append(coord.tolist())
            self.put_pixel(
                    Position(*coord),
                    line.color,
                    line.operation,
                    skip_default,
                    positions,
                    collected_pixels
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
                        source_mesh=source_mesh or line,
                        positions=positions,
                        record_pixels=record_pixels,
                        collected_pixels=collected_pixels
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
                            source_mesh=source_mesh or line,
                            positions=positions,
                            record_pixels=record_pixels,
                            collected_pixels=collected_pixels
                        )

    @put_mesh.register(Polygon)
    def put_polygon(
                self,
                polygon: Polygon,
                skip_default: bool = True,
                positions: set[tuple[int, int]] | None = None,
                record_pixels: bool = True,
                collected_pixels: set[tuple[int, int]] | None = None
            ) -> None:
        polygon_positions = polygon.positions + [polygon.positions[0]]

        for i in range(len(polygon_positions) - 1):
            self.put_line(
                    Line(
                        polygon.color,
                        polygon_positions[i],
                        polygon_positions[i + 1],
                        operation=polygon.operation,
                        thickness=polygon.thickness,
                    ),
                    source_mesh=polygon,
                    positions=positions,
                    record_pixels=record_pixels,
                    collected_pixels=collected_pixels
                )

    @put_mesh.register(Plane)
    def put_plane(
                self,
                plane: Plane,
                skip_default: bool = True,
                positions: set[tuple[int, int]] | None = None,
                record_pixels: bool = True,
                collected_pixels: set[tuple[int, int]] | None = None
            ) -> None:
        a, b = plane.positions

        x_start = max(0, min(a.x, b.x))
        x_end = min(self.width, max(a.x, b.x))
        y_start = max(0, min(a.y, b.y))
        y_end = min(self.height, max(a.y, b.y))

        if x_start >= x_end or y_start >= y_end:
            return

        x_coords, y_coords = np.meshgrid(
            np.arange(x_start, x_end),
            np.arange(y_start, y_end),
            indexing='xy'
        )
        self.put_pixels(
            x_coords.ravel(),
            y_coords.ravel(),
            plane.color,
            plane.operation,
            skip_default=skip_default,
            positions=positions,
            collected_pixels=collected_pixels,
            record_pixels=record_pixels,
            source_mesh=plane
        )

    def put_pixels(
                self,
                x_coords: np.ndarray,
                y_coords: np.ndarray,
                color: Color,
                operation: OperationEnum = OperationEnum.SET,
                skip_default: bool = True,
                positions: set[tuple[int, int]] | None = None,
                collected_pixels: set[tuple[int, int]] | None = None,
                record_pixels: bool = True,
                source_mesh: Mesh | None = None
            ) -> None:
        if x_coords.size == 0 or color.is_default:
            return

        valid = (
            (x_coords >= 0) & (x_coords < self.width) &
            (y_coords >= 0) & (y_coords < self.height)
        )

        if positions is not None:
            valid &= np.array([
                (int(x), int(y)) in positions
                for x, y in zip(x_coords, y_coords)
            ])

        x_coords = x_coords[valid].astype(int)
        y_coords = y_coords[valid].astype(int)

        if record_pixels and source_mesh is not None:
            source_mesh.clean_pixel.extend(
                zip(x_coords.tolist(), y_coords.tolist())
            )

        if collected_pixels is not None:
            collected_pixels.update(zip(x_coords.tolist(), y_coords.tolist()))
            return

        if operation == OperationEnum.SET:
            self.grid[y_coords, x_coords] = color
            return

        for x, y in zip(x_coords.tolist(), y_coords.tolist()):
            self.put_pixel(
                Position(x, y),
                color,
                operation,
                skip_default=skip_default
            )

    def put_pixel(
                self,
                position: Position,
                color: Color,
                operation: OperationEnum = OperationEnum.SET,
                skip_default: bool = True,
                positions: set[tuple[int, int]] | None = None,
                collected_pixels: set[tuple[int, int]] | None = None
            ) -> None:

        if position.x < 0 or position.x >= self.width or\
            position.y < 0 or position.y >= self.height:
            # TODO: LOG WARNING
            return

        if positions is not None and (position.x, position.y) not in positions:
            return

        if collected_pixels is not None:
            collected_pixels.add((int(position.x), int(position.y)))
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
        self.grid[:, :] = Color.default()
        for mesh in self.meshes:
            mesh.clean_pixel.clear()
            self.put_mesh(
                    mesh
                )

    def calculate_mesh_pixels(
                self,
                mesh: Mesh,
                positions: list[list[int]] | None = None
            ) -> list[list[int]]:
        collected_pixels: set[tuple[int, int]] = set()
        target_positions = None

        if positions is not None:
            target_positions = {
                (x, y)
                for x, y in positions
                if 0 <= x < self.width and 0 <= y < self.height
            }

        self.put_mesh(
            mesh,
            positions=target_positions,
            record_pixels=False,
            collected_pixels=collected_pixels
        )

        return [[x, y] for x, y in collected_pixels]

    def refresh_at(
                self,
                positions: list[list[int]]
            ) -> None:
        target_positions = {
            (x, y)
            for x, y in positions
            if 0 <= x < self.width and 0 <= y < self.height
        }

        for x, y in target_positions:
            self.grid[y][x] = Color.default()

        for mesh in self.meshes:
            mesh.clean_pixel = [
                coord for coord in mesh.clean_pixel
                if tuple(coord) not in target_positions
            ]
            self.put_mesh(
                mesh,
                positions=target_positions,
                record_pixels=True
            )

    def refresh_mesh(
                self,
                mesh: Mesh
            ) -> None:
        if self.gpu_mode:
            mesh.dirty = True
            return

        old_pixels = [coord[:] for coord in mesh.clean_pixel]
        new_pixels = self.calculate_mesh_pixels(mesh)
        to_refresh = old_pixels + new_pixels
        self.refresh_at(to_refresh)
        for x, y in to_refresh:
            self.dirty_grid[y][x] = True


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
        self.gpu_renderer: GPURenderer | None = None

        if pygame_screen.get_flags() & pygame.OPENGL:
            self.gpu_renderer = GPURenderer(
                self.width,
                self.height
            )
            self.static_mesh_layer.gpu_mode = True
            self.dynamic_mesh_layer.gpu_mode = True

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
        if self.gpu_renderer is not None:
            self.gpu_renderer.render(
                self.static_mesh_layer.meshes,
                self.dynamic_mesh_layer.meshes
            )
            return

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
            self.put_pixel(Position(*position), self.static_mesh_layer.grid[y][x])
            # self.pygame_matrix[x][y] =\
            #     self.static_mesh_layer.grid[y][x].to_32

    def refresh_at(
                self,
                positions: list[list[int]]
            ) -> None:
        self.dynamic_mesh_layer.refresh_at(positions)

        for x, y in positions:
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                continue

            static_color = self.static_mesh_layer.grid[y][x]
            dynamic_color = self.dynamic_mesh_layer.grid[y][x]
            self.grid.grid[y][x] = static_color

            if not dynamic_color.is_default:
                self.grid.grid[y][x] = static_color.apply_operation(
                    dynamic_color,
                    self.dynamic_mesh_layer.operation
                )

            self.put_pixel(Position(x, y), self.grid.grid[y][x])

    def refresh_dynamic(
                self
            ) -> None:
        if self.gpu_renderer is not None:
            self.gpu_renderer.render(
                self.static_mesh_layer.meshes,
                self.dynamic_mesh_layer.meshes
            )
            return

        coords = np.argwhere(self.dynamic_mesh_layer.dirty_grid)[:, ::-1]
        self.clear_at(coords)
        self.refresh_at(coords)
        self.dynamic_mesh_layer.dirty_grid = np.zeros(
                (self.height, self.width), dtype=bool
            )
