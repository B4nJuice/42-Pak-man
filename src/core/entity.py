from typing import TYPE_CHECKING

from src.app import App

from ..utils import Pos, Vec2

if TYPE_CHECKING:
    from .level import Level

from .tile import Tile


class Entity:
    _name: str
    tile: Tile
    level: 'Level'
    app: App

    def __init__(
                self,
                name: str,
                tile: Pos | Tile,
                level: 'Level',
                app: App
            ) -> None:
        """
        Initialize the instance.

        Args:
            name: Name assigned to the object or requested value.
            tile: Grid tile occupied by or assigned to the entity.
            level: Level containing the entity or navigation data.
            app: Application instance that owns the object.
        """
        self._name = name
        self.level = level
        self.app = app
        self.set_tile(tile)

        self.level.register_entity(self)

    def init(self) -> None:
        """
        Initialize the associated state.
        """
        pass

    def get_name(self) -> str:
        """
        Return the current name.

        Returns:
            The current name.
        """
        return self._name

    def get_tile(self) -> Tile:
        """
        Return the current tile.

        Returns:
            The current tile.
        """
        return self.tile

    def set_tile(self, tile: Pos | Tile) -> None:
        """
        Assign the tile.

        Args:
            tile: Grid tile occupied by or assigned to the entity.
        """
        if isinstance(tile, Tile):
            self.tile = tile
        else:
            self.tile = self.level.get_tile(*tile)

    @property
    def pos(self) -> Vec2:
        """
        Handle pos.

        Returns:
            The value produced by the pos operation.
        """
        return float(self.tile.get_x()), float(self.tile.get_y())

    def update(self, dt: float) -> None:
        """
        Handle update.

        Args:
            dt: Elapsed time since the previous update, in seconds.
        """
        pass

    def destroy(self) -> None:
        """
        Handle destroy.
        """
        self.level.unregister_entity(self)

    def __repr__(self) -> str:
        """
        Return the developer-readable representation.

        Returns:
            The value produced by the repr operation.
        """
        return f'<{self.get_name()} tile={self.get_tile()}>'
