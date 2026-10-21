from src.core.entity_store import EntityStore

from .collider import Collider
from .displayable import Displayable, DisplayableEntity
from .entity import Entity
from .maze import Maze
from .state_manager import StateManager


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

    def register_entity(self, entity: DisplayableEntity) -> None:
        self._entities.add(entity)
        if isinstance(entity, Collider):
            self._colliders.append(entity)
        if isinstance(entity, Displayable):
            self._to_register.append(entity)

    def unregister_entity(self, entity: DisplayableEntity) -> None:
        self._entities.remove(entity)
        if entity in self._colliders:
            self._colliders.remove(entity)
        if isinstance(entity, Displayable):
            self._to_unregister.append(entity)

    @property
    def store(self) -> EntityStore:
        return self._entities

    def _check_collisions(self) -> None:
        for a in self._colliders:
            if a._primary:
                for b in self._colliders:
                    if a is b:
                        continue
                    if a.overlaps(b):
                        a.on_collision(b)
                        b.on_collision(a)

    def get_entities(self) -> list[Entity]:
        return self._entities.all()
