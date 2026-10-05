from .collider import Collider
from .entity import Entity
from .maze import Maze


class Level(Maze):
    _entities: list[Entity]
    _colliders: list[Entity]

    def __init__(self, seed: int):
        super().__init__(seed)

        self._entities = []
        self._colliders = []

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

    def unregister_entity(self, entity: Entity) -> None:
        self._entities.remove(entity)
        if entity in self._colliders:
            self._colliders.remove(entity)

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
