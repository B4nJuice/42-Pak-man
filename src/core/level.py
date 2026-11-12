from collections import defaultdict
from typing import cast

from src.config.level_model import LevelModel
from src.core.entity_store import EntityStore

from .collider import Collider
from .displayable import Displayable, DisplayableEntity
from .entity import Entity
from .maze import Maze
from .movable import Movable
from .state_manager import StateManager
from .tile import Tile


class Level(Maze):
    state: StateManager
    _entities: EntityStore
    _static_colliders: list[Collider]
    _dynamic_colliders: list[Collider]
    _static_collision_grid: defaultdict[Tile, list[Collider]]
    _primary_colliders: list[Collider]
    _to_register: list[DisplayableEntity]
    _to_unregister: list[DisplayableEntity]

    def __init__(self, level: LevelModel, seed: int) -> None:
        """
        Initialize the instance.

        Args:
            level: Level containing the entity or navigation data.
            seed: Seed given to the maze generator for this level.
        """
        super().__init__(seed)

        self._entities = EntityStore()
        self._static_colliders = []
        self._dynamic_colliders = []
        self._static_collision_grid = defaultdict(list)
        self._primary_colliders = []
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
            if isinstance(entity, Movable):
                self._dynamic_colliders.append(entity)
            else:
                self._static_colliders.append(entity)
                self._add_to_collision_grid(
                    self._static_collision_grid,
                    entity
                )
            if entity.is_primary():
                self._primary_colliders.append(entity)
        if isinstance(entity, Displayable):
            self._to_register.append(entity)

    def unregister_entity(self, entity: DisplayableEntity | Entity) -> None:
        """
        Handle unregister entity.

        Args:
            entity: Entity used by the operation.
        """
        self._entities.remove(entity)
        if entity in self._static_colliders:
            collider = cast(Collider, entity)
            self._static_colliders.remove(collider)
            self._remove_from_collision_grid(
                self._static_collision_grid,
                collider
            )
        if entity in self._dynamic_colliders:
            self._dynamic_colliders.remove(cast(Collider, entity))
        if entity in self._primary_colliders:
            self._primary_colliders.remove(cast(Collider, entity))
        if isinstance(entity, Displayable):
            self._to_unregister.append(entity)

    def update_primary_collider(
                self,
                collider: Collider,
                primary: bool
            ) -> None:
        """
        Update the primary collider index.

        Args:
            collider: Collider to update.
            primary: Whether the collider initiates collision checks.
        """
        if primary and collider not in self._primary_colliders:
            self._primary_colliders.append(collider)
        elif not primary and collider in self._primary_colliders:
            self._primary_colliders.remove(collider)

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
        dynamic_grid: defaultdict[Tile, list[Collider]] = defaultdict(list)
        for collider in self._dynamic_colliders:
            self._add_to_collision_grid(dynamic_grid, collider)

        for a in self._primary_colliders:
            candidates: set[Collider] = set()
            for tile in a.occupied_tile():
                for y in range(tile.get_y() - 1, tile.get_y() + 2):
                    for x in range(tile.get_x() - 1, tile.get_x() + 2):
                        if self.is_within_bounds((x, y)):
                            grid_tile = self.get_tile(x, y)
                            candidates.update(
                                self._static_collision_grid.get(
                                    grid_tile, ()
                                )
                            )
                            candidates.update(
                                dynamic_grid.get(grid_tile, ())
                            )

            for b in candidates:
                if a is b:
                    continue
                if a.overlaps(b):
                    a.on_collision(b)
                    b.on_collision(a)

    @staticmethod
    def _add_to_collision_grid(
                grid: defaultdict[Tile, list[Collider]],
                collider: Collider
            ) -> None:
        """
        Add a collider to each tile occupied by it.
        """
        for tile in collider.occupied_tile():
            grid[tile].append(collider)

    @staticmethod
    def _remove_from_collision_grid(
                grid: defaultdict[Tile, list[Collider]],
                collider: Collider
            ) -> None:
        """
        Remove a collider from each tile occupied by it.
        """
        for tile in collider.occupied_tile():
            colliders = grid.get(tile)
            if colliders is None:
                continue
            colliders.remove(collider)
            if not colliders:
                del grid[tile]

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
