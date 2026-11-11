from collections import defaultdict
from typing import cast

from src.config.level_model import LevelModel
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

    def __init__(self, level: LevelModel):
        """
        Initialize the instance.

        Args:
            level: Level containing the entity or navigation data.
        """
        super().__init__(level.seed)

        self._entities = EntityStore()
        self._colliders = []
        self._to_register = []
        self._to_unregister = []

        self.state = StateManager(self)

    def init(self) -> None:
        """
        Initialize the associated state.
        """
        for entity in self._entities.all():
            entity.init()

    def update(self, dt: float) -> None:
        """
        Handle update.

        Args:
            dt: Elapsed time since the previous update, in seconds.
        """
        for entity in self._entities.all():
            entity.update(dt)
        self._check_collisions()

        self.state.update(dt)

    def register_entity(self, entity: DisplayableEntity | Entity) -> None:
        """
        Handle register entity.

        Args:
            entity: Entity used by the operation.
        """
        self._entities.add(entity)
        if isinstance(entity, Collider):
            self._colliders.append(entity)
        if isinstance(entity, Displayable):
            self._to_register.append(entity)

    def unregister_entity(self, entity: DisplayableEntity | Entity) -> None:
        """
        Handle unregister entity.

        Args:
            entity: Entity used by the operation.
        """
        self._entities.remove(entity)
        if entity in self._colliders:
            self._colliders.remove(cast(Collider, entity))
        if isinstance(entity, Displayable):
            self._to_unregister.append(entity)

    @property
    def store(self) -> EntityStore:
        """
        Handle store.

        Returns:
            The value produced by the store operation.
        """
        return self._entities

    def _check_collisions(self) -> None:
        """
        Handle check collisions.
        """
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
        """
        Return the current entities.

        Returns:
            The current entities.
        """
        return self._entities.all()

    def is_finished(self) -> bool:
        """
        Check whether the finished condition holds.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        from src.game.items.pacgum import PacGum
        from src.game.items.super_pacgum import SuperPacGum

        return not self._entities.gets(PacGum)\
            and not self._entities.gets(SuperPacGum)
