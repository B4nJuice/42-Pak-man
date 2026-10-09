from functools import partial

from src.core.displayable import Displayable
from src.core.level import Level
from src.graphics import Color, OperationEnum, Position
from src.graphics.mesh_layer import MeshLayer
from src.graphics.meshes import Line
from src.graphics.super_mesh import SuperMesh
from src.utils.direction import Direction


class MeshLevel(SuperMesh):
    width: int
    height: int
    wall_thickness: int
    level: Level
    layer: MeshLayer
    tile_width: int
    tile_height: int
    width_offset: int
    height_offset: int
    position: Position

    def __init__(
                self,
                level: Level,
                color: Color,
                position: Position,
                width: int,
                height: int,
                wall_thickness: int,
                operation: OperationEnum = OperationEnum.SET,
                dynamic: bool = False,
                smooth_end: bool = False,
            ) -> None:
        super().__init__(
            color,
            operation=operation,
            dynamic=dynamic
        )

        self.width = width
        self.height = height
        self.wall_thickness = wall_thickness
        self.level = level

        self.layer = MeshLayer()

        self.tile_width = self.width // self.level.get_width()
        self.tile_height = self.height // self.level.get_height()

        self.width_offset = (self.width - (
                self.tile_width * self.level.get_width()
            )) // 2
        self.height_offset = (self.height - (
                self.tile_height * self.level.get_height()
            )) // 2

        self.position = position
        self.position.x += self.width_offset
        self.position.y += self.height_offset

        self.create_wall = partial(
            Line,
            self.get_color(),
            operation=self.get_operation(),
            thickness=self.wall_thickness,
            dynamic=self.is_dynamic(),
            smooth_end=smooth_end
        )

        self.init()

    def init(self) -> None:
        for row in self.level.get_grid():
            for tile in row:
                wall: Line
                if tile.get_y() == 0 or tile.has_wall(Direction.NORTH):
                    wall = self.create_wall(
                        Position(
                                tile.get_x() * self.tile_width +
                                self.position.x,
                                tile.get_y() * self.tile_height +
                                self.position.y
                            ),
                        Position(
                                tile.get_x() * self.tile_width +
                                self.position.x + self.tile_width,
                                tile.get_y() * self.tile_height +
                                self.position.y
                            )
                    )
                    self.layer.meshes.append(wall)

                if tile.get_x() == (self.level.get_width() - 1) or\
                        tile.has_wall(Direction.EAST):
                    wall = self.create_wall(
                        Position(
                                tile.get_x() * self.tile_width +
                                self.position.x + self.tile_width,
                                tile.get_y() * self.tile_height +
                                self.position.y
                            ),
                        Position(
                                tile.get_x() * self.tile_width +
                                self.position.x + self.tile_width,
                                tile.get_y() * self.tile_height +
                                self.position.y + self.tile_height
                            )
                    )
                    self.layer.meshes.append(wall)

                if tile.get_x() == 0:
                    wall = self.create_wall(
                        Position(
                                tile.get_x() * self.tile_width +
                                self.position.x,
                                tile.get_y() * self.tile_height +
                                self.position.y
                            ),
                        Position(
                                tile.get_x() * self.tile_width +
                                self.position.x,
                                tile.get_y() * self.tile_height +
                                self.position.y + self.tile_height
                            )
                    )
                    self.layer.meshes.append(wall)

                if tile.get_y() == (self.level.get_height() - 1):
                    wall = self.create_wall(
                        Position(
                                tile.get_x() * self.tile_width +
                                self.position.x,
                                tile.get_y() * self.tile_height +
                                self.position.y + self.tile_height
                            ),
                        Position(
                                tile.get_x() * self.tile_width +
                                self.position.x + self.tile_width,
                                tile.get_y() * self.tile_height +
                                self.position.y + self.tile_height
                            )
                    )
                    self.layer.meshes.append(wall)

    def register_entities_to_screen(self) -> None:
        for entity in self.level.get_entities():
            if isinstance(entity, Displayable):
                self.register_entity(entity)

    def register_entity(self, entity: Displayable) -> None:
        mesh = entity.get_mesh()

        mesh.get_position = lambda e=entity: Position(
            round(e.pos[0] * self.tile_width + self.position.x +
                  self.tile_width // 2),
            round(e.pos[1] * self.tile_height + self.position.y +
                  self.tile_height // 2)
        )

        mesh.get_height = lambda e=entity: round(
                self.tile_width * e.get_proportion()
            )
        mesh.get_width = lambda e=entity: round(
                self.tile_height * e.get_proportion()
            )

        if mesh not in self.get_layer().meshes:
            self.get_layer().meshes.append(mesh)

    def unregister_entity(self, entity: Displayable) -> None:
        mesh = entity.get_mesh()
        if mesh in self.layer.meshes:
            self.layer.meshes.remove(mesh)

    def refresh(self) -> None:
        ...

    def get_layer(self) -> MeshLayer:
        return self.layer
