from src.graphics import Position, OperationEnum, Color, SuperMesh, MeshLayer
from src.graphics.meshes import Line
from src.core.level import Level
from src.graphics.super_meshes import Rectangle
from src.utils.direction import Direction


class MeshLevel(SuperMesh):
    def __init__(
                self,
                level: Level,
                color: Color,
                position: Position,
                width: int,
                height: int,
                wall_thickness: int,
                operation: OperationEnum = OperationEnum.SET,
                is_dynamic: bool = False
            ) -> None:
        super().__init__(
            color,
            operation=operation,
            is_dynamic=is_dynamic
        )

        self.width: int = width
        self.height: int = height
        self.wall_thickness: int = thickness
        self.level: Level = level

        self.layer: MeshLayer = MeshLayer()

        self.tile_width: int = self.width // self.level.get_width()
        self.tile_height: int = self.width // self.level.get_height()

        self.width_offset: int = self.width - (
                self.tile_width * self.level.get_width()
            ) // 2
        self.height_offset: int = self.height - (
                self.tile_height * self.level.get_height()
            ) // 2

        self.position: Position = position
        self.position.x += self.width_offset
        self.position.y += self.height_offset

        self.init()

    def init(self) -> None:
        border: Rectangle = Rectangle(
                self.color,
                self.position,
                self.width,
                self.height,
                self.wall_thickness,
                operation=self.operation,
                is_dynamic=self.is_dynamic
            )
        self.layer.meshes.append(border)

        for row in self.level.get_grid():
            for tile in row:
                if tile.has_wall(Direction.NORTH):
                    wall: Line(
                        self.color,
                        Position(
                                tile.get_x() * self.tile_width +\
                                    self.width_offset,
                                tile.get_y() * self.tile_height +\
                                    self.height_offset
                            ),
                        Position(
                                tile.get_x() * self.tile_width +\
                                    self.width_offset + self.tile_width,
                                tile.get_y() * self.tile_height +\
                                    self.height_offset
                            ),
                        operation=self.operation,
                        thickness=self.wall_thickness,
                        is_dynamic=self.is_dynamic
                    )
                    self.layer.meshes.append(wall)

                if tile.has_wall(Direction.EAST):
                    wall: Line(
                        self.color,
                        Position(
                                tile.get_x() * self.tile_width +\
                                    self.width_offset,
                                tile.get_y() * self.tile_height +\
                                    self.height_offset
                            ),
                        Position(
                                tile.get_x() * self.tile_width +\
                                    self.width_offset,
                                tile.get_y() * self.tile_height +\
                                    self.height_offset + + self.tile_height
                            ),
                        operation=self.operation,
                        thickness=self.wall_thickness,
                        is_dynamic=self.is_dynamic
                    )
                    self.layer.meshes.append(wall)

    def refresh(self) -> None:
        ...

    def get_layer(self) -> MeshLayer:
        return self.layer
