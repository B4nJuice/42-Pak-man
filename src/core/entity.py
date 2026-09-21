from ..utils import Pos, Vec2
from .level import Level
from .tile import Tile


class Entity:
    _name: str
    tile: Tile
    level: Level

    def __init__(self, name: str, tile: Pos | Tile, level: Level) -> None:
        self._name = name
        self.level = level
        self.set_tile(tile)

        # TODO: register to level

    def get_name(self) -> str:
        return self._name

    def get_tile(self) -> Tile:
        return self.tile

    def set_tile(self, tile: Pos | Tile) -> None:
        if isinstance(tile, Tile):
            self.tile = tile
        else:
            self.tile = self.level.get_tile(*tile)

    @property
    def pos(self) -> Vec2:
        return float(self.tile.get_x()), float(self.tile.get_y())

    def update(self, dt: float) -> None:
        pass

    def destroy(self) -> None:
        pass

    def __repr__(self) -> str:
        return f'<{self.get_name()} tile={self.get_tile()}>'
