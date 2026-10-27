from collections import defaultdict
from typing import cast

from src.core.entity_store import EntityStore

from .collider import Collider
from .displayable import Displayable, DisplayableEntity
from .entity import Entity
from .maze import Maze
from .state_manager import StateManager
from .tile import Tile


class Level(Maze):
    state: StateManager
    _entities: EntityStore
    _colliders: list[Collider]
    _to_register: list[DisplayableEntity]
    _to_unregister: list[DisplayableEntity]

    def __init__(self, seed: int):
        super().__init__(seed)

        self._entities = EntityStore()
        self._colliders = []
        self._to_register = []
        self._to_unregister = []

        self.state = StateManager(self)

    def init(self) -> None:
        for entity in self._entities.all():
            entity.init()

    def update(self, dt: float) -> None:
        for entity in self._entities.all():
            entity.update(dt)
        self._check_collisions()

        self.state.update(dt)

    def register_entity(self, entity: DisplayableEntity | Entity) -> None:
        self._entities.add(entity)
        if isinstance(entity, Collider):
            self._colliders.append(entity)
        if isinstance(entity, Displayable):
            self._to_register.append(entity)

    def unregister_entity(self, entity: DisplayableEntity | Entity) -> None:
        self._entities.remove(entity)
        if entity in self._colliders:
            self._colliders.remove(cast(Collider, entity))
        if isinstance(entity, Displayable):
            self._to_unregister.append(entity)

    @property
    def store(self) -> EntityStore:
        return self._entities

    def _check_collisions(self) -> None:
        grid: defaultdict[Tile, list[Collider]] = defaultdict(list)
        for collider in self._colliders:
            for tile in collider.occupied_tile():
                grid[tile].append(collider)

        for a in self._colliders:
            if not a._primary:
                continue

            candidates: set[Collider] = set()
            for tile in a.occupied_tile():
                for y in range(tile.get_y() - 1, tile.get_y() + 2):
                    for x in range(tile.get_x() - 1, tile.get_x() + 2):
                        if self.is_within_bounds((x, y)):
                            candidates.update(
                                grid.get(self.get_tile(x, y), ())
                            )

            for b in candidates:
                if a is b:
                    continue
                if a.overlaps(b):
                    a.on_collision(b)
                    b.on_collision(a)

    def get_entities(self) -> list[Entity]:
        return self._entities.all()
