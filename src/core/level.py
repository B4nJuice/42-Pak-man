from .collider import Collider
from .displayable import Displayable
from .entity import Entity
from .maze import Maze


class Level(Maze):
    _entities: list[Entity]
    _colliders: list[Entity]
    _to_register: list[Displayable]
    _to_unregister: list[Displayable]

    def __init__(self, seed: int):
        super().__init__(seed)

        self._entities = []
        self._colliders = []
        self._to_register = []
        self._to_unregister = []

    def init(self) -> None:
        for entity in self._entities:
            entity.init()

    def update(self, dt: float) -> None:
        for entity in list(self._entities):
            entity.update(dt)
        self._check_collisions()

    def register_entity(self, entity: Entity) -> None:
        self._entities.append(entity)
        if isinstance(entity, Collider):
            self._colliders.append(entity)
        if isinstance(entity, Displayable):
            self._to_register.append(entity)

    def unregister_entity(self, entity: Entity) -> None:
        self._entities.remove(entity)
        if entity in self._colliders:
            self._colliders.remove(entity)
        if isinstance(entity, Displayable):
            self._to_unregister.append(entity)

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
        return self._entities
