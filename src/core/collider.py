from typing import Protocol

from ..utils import Vec2
from .entity import Entity
from .tile import Tile


class ColliderEntityProtocol(Protocol):
    tile: Tile
    pos: Vec2

    def get_radius(self) -> float: ...


class Collider:
    _solid: bool
    _radius: float

    def __init__(self, *args, solid: bool = True, radius: float = 0.4, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        if not isinstance(self, Entity):
            raise TypeError(
                f'Collider must be a subclass of Entity, got {type(self)}'
            )

        self.set_solid(solid)
        self.set_radius(radius)

    def set_solid(self, solid: bool) -> None:
        self._solid = solid

    def set_radius(self, radius: float) -> None:
        self._radius = radius

    def is_solid(self) -> bool:
        return self._solid

    def get_radius(self) -> float:
        return self._radius

    def occupied_tile(self: ColliderEntityProtocol) -> set[Tile]:
        tiles: set[Tile] = {self.tile}

        get_target = getattr(self, 'get_target', None)
        if get_target is not None and get_target() is not None:
            tiles.add(get_target())
            return tiles

        return tiles

    def overlaps(self: ColliderEntityProtocol, other: ColliderEntityProtocol) -> bool:
        ax, ay = self.pos
        bx, by = other.pos
        r = self.get_radius() + other.get_radius()
        return (ax - bx) ** 2 + (ay - by) ** 2 < r * r

    def on_collision(self, other: 'Collider') -> None:
        pass

    def on_collision_exit(self, other: 'Collider') -> None:
        pass
