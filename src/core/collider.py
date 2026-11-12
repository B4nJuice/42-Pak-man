from typing import Any

from .entity import Entity
from .tile import Tile


class Collider:
    _solid: bool
    _radius: float
    _primary: float

    def __init__(
                self,
                *args: Any,
                solid: bool = True,
                radius: float = 0.4,
                primary: bool = False,
                **kwargs: Any
            ) -> None:
        """
        Initialize the instance.

        Args:
            solid: Solid used by the operation.
            radius: Collision radius of the entity.
            primary: Primary used by the operation.
            args: Command-line arguments passed to the application.
            kwargs: Kwargs used by the operation.
        """
        super().__init__(*args, **kwargs)

        if not isinstance(self, Entity):
            raise TypeError(
                f'Collider must be a subclass of Entity, got {type(self)}'
            )

        self.set_solid(solid)
        self.set_radius(radius)
        self.set_primary(primary)

    def set_solid(self, solid: bool) -> None:
        """
        Assign the solid.

        Args:
            solid: Solid used by the operation.
        """
        self._solid = solid

    def set_radius(self, radius: float) -> None:
        """
        Assign the radius.

        Args:
            radius: Collision radius of the entity.
        """
        self._radius = radius

    def set_primary(self, primary: bool) -> None:
        """
        Assign the primary.

        Args:
            primary: Primary used by the operation.
        """
        self._primary = primary
        level = getattr(self, 'level', None)
        if level is not None:
            level.update_primary_collider(self, primary)

    def is_solid(self) -> bool:
        """
        Check whether the solid condition holds.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        return self._solid

    def is_primary(self) -> bool:
        """
        Return whether this collider initiates collision checks.

        Returns:
            Whether the collider is primary.
        """
        return getattr(self, '_primary', False)

    def get_radius(self) -> float:
        """
        Return the current radius.

        Returns:
            The current radius.
        """
        return self._radius

    def occupied_tile(self) -> set[Tile]:
        """
        Handle occupied tile.

        Returns:
            The value produced by the occupied tile operation.
        """
        if not isinstance(self, Entity):
            return set()

        tiles: set[Tile] = {self.tile}

        get_target = getattr(self, 'get_target', None)
        if get_target is not None and get_target() is not None:
            tiles.add(get_target())
            return tiles

        return tiles

    def overlaps(self, other: 'Collider') -> bool:
        """
        Handle overlaps.

        Args:
            other: Other collider involved in the collision.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        if not isinstance(self, Entity) or not isinstance(other, Entity):
            return False

        ax, ay = self.pos
        bx, by = other.pos
        r = self.get_radius() + other.get_radius()
        return (ax - bx) ** 2 + (ay - by) ** 2 < r * r

    def on_collision(self, other: 'Collider') -> None:
        """
        Handle the collision event.

        Args:
            other: Other collider involved in the collision.
        """

    def on_collision_exit(self, other: 'Collider') -> None:
        """
        Handle the collision exit event.

        Args:
            other: Other collider involved in the collision.
        """
