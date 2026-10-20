from functools import partial
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.game.characters import Player

from src.core.displayable import Displayable
from src.core.level import Level
from src.graphics import Color, OperationEnum, Position
from src.graphics.mesh_layer import MeshLayer
from src.graphics.meshes import ImageTexture, Line, Plane
from src.graphics.super_mesh import SuperMesh
from src.utils.direction import Direction


class MeshLevel(SuperMesh):
    entity_meshes: dict[Displayable, ImageTexture]
    wall_thickness: int
    position: Position
    height_offset: int
    tiles: list[Plane]
    width_offset: int
    walls: list[Line]
    tile_height: int
    layer: MeshLayer
    tile_width: int
    player: 'Player'
    level: Level
    height: int
    width: int

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
        self.entity_meshes = {}

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

        self.walls = []
        self.tiles = []

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
        from src.game.characters import Player
        for row in self.level.get_grid():
            for tile in row:
                tile_mesh = Plane(
                    Color.default(),
                    (
                        Position(
                            tile.get_x() * self.tile_width + self.position.x,
                            tile.get_y() * self.tile_height + self.position.y
                        ),
                        Position(
                            (tile.get_x() + 1) * self.tile_width +
                            self.position.x,
                            (tile.get_y() + 1) * self.tile_height +
                            self.position.y
                        )
                    ),
                    operation=OperationEnum.ALPHA
                )
                self.tiles.append(tile_mesh)
                self.layer.meshes.append(tile_mesh)

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
                    self.walls.append(wall)

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
                    self.walls.append(wall)

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
                    self.walls.append(wall)

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
                    self.walls.append(wall)

        self.layer.meshes += self.walls
        self.player = self.level._entities.get(Player)

    def register_entity(self, entity: Displayable) -> None:
        mesh = entity.get_mesh()
        previous_mesh = self.entity_meshes.get(entity)
        if previous_mesh is not None and previous_mesh is not mesh:
            if previous_mesh in self.layer.meshes:
                self.layer.meshes.remove(previous_mesh)

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
        self.entity_meshes[entity] = mesh

    def unregister_entity(self, entity: Displayable) -> None:
        mesh = self.entity_meshes.pop(entity, None)
        if mesh is not None and mesh in self.layer.meshes:
            self.layer.meshes.remove(mesh)

    def refresh(self) -> None:
        for tile_mesh in self.tiles:
            tile_mesh.set_color(Color.default())

        if not self.player._cheat:
            return

        from src.game.characters import Ghost

        for ghost in self.level._entities.gets(Ghost):
            tile = ghost.get_target_tile()
            path_tiles = [tile]

            for direction in ghost.get_next_moves():
                next_tile = self.level.get_next_tile(tile, direction)
                if next_tile is None:
                    break
                path_tiles.append(next_tile)
                tile = next_tile

            for path_tile in path_tiles:
                index = (
                    path_tile.get_y() * self.level.get_width()
                    + path_tile.get_x()
                )
                self.tiles[index].set_color(ghost._path_color)

    def get_layer(self) -> MeshLayer:
        return self.layer
