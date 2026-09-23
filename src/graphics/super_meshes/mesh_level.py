from functools import partial

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
                is_dynamic: bool = False,
                smooth_end: bool = False,
            ) -> None:
        super().__init__(
            color,
            operation=operation,
            is_dynamic=is_dynamic
        )

        self.width: int = width
        self.height: int = height
        self.wall_thickness: int = wall_thickness
        self.level: Level = level

        self.layer: MeshLayer = MeshLayer()

        self.tile_width: int = self.width // self.level.get_width()
        self.tile_height: int = self.height // self.level.get_height()

        self.width_offset: int = (self.width - (
                self.tile_width * self.level.get_width()
            )) // 2
        self.height_offset: int = (self.height - (
                self.tile_height * self.level.get_height()
            )) // 2

        self.position: Position = position
        self.position.x += self.width_offset
        self.position.y += self.height_offset

        self.create_wall = partial(
            Line,
            self.color,
            operation=self.operation,
            thickness=self.wall_thickness,
            is_dynamic=self.is_dynamic,
            smooth_end=smooth_end
        )

        self.init()

    def init(self) -> None:
        for row in self.level.get_grid():
            for tile in row:
                if tile.get_y() == 0 or tile.has_wall(Direction.NORTH):
                    wall: Line = self.create_wall(
                        Position(
                                tile.get_x() * self.tile_width +\
                                    self.position.x,
                                tile.get_y() * self.tile_height +\
                                    self.position.y
                            ),
                        Position(
                                tile.get_x() * self.tile_width +\
                                    self.position.x + self.tile_width,
                                tile.get_y() * self.tile_height +\
                                    self.position.y
                            )
                    )
                    self.layer.meshes.append(wall)

                if tile.get_x() == (self.level.get_width() - 1) or\
                    tile.has_wall(Direction.EAST):
                    wall: Line = self.create_wall(
                        Position(
                                tile.get_x() * self.tile_width +\
                                    self.position.x + self.tile_width,
                                tile.get_y() * self.tile_height +\
                                    self.position.y
                            ),
                        Position(
                                tile.get_x() * self.tile_width +\
                                    self.position.x + self.tile_width,
                                tile.get_y() * self.tile_height +\
                                    self.position.y + self.tile_height
                            )
                    )
                    self.layer.meshes.append(wall)

                if tile.get_x() == 0:
                    wall: Line = self.create_wall(
                        Position(
                                tile.get_x() * self.tile_width +\
                                    self.position.x,
                                tile.get_y() * self.tile_height +\
                                    self.position.y
                            ),
                        Position(
                                tile.get_x() * self.tile_width +\
                                    self.position.x,
                                tile.get_y() * self.tile_height +\
                                    self.position.y + self.tile_height
                            )
                    )
                    self.layer.meshes.append(wall)

                if tile.get_y() == (self.level.get_height() - 1):
                    wall: Line = self.create_wall(
                        Position(
                                tile.get_x() * self.tile_width +\
                                    self.position.x,
                                tile.get_y() * self.tile_height +\
                                    self.position.y + self.tile_height
                            ),
                        Position(
                                tile.get_x() * self.tile_width +\
                                    self.position.x + self.tile_width,
                                tile.get_y() * self.tile_height +\
                                    self.position.y + self.tile_height
                            )
                    )
                    self.layer.meshes.append(wall)



    def refresh(self) -> None:
        ...

    def get_layer(self) -> MeshLayer:
        return self.layer
