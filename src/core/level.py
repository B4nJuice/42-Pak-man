from .collider import Collider
from .entity import Entity
from .maze import Maze


class Level(Maze):
    _entities: list[Entity]
    _contacts: set[frozenset[int]]

    def __init__(self, seed: int):
        super().__init__(seed)

    def update(self, dt: float) -> None:
        for entity in list(self._entities):
            entity.update(dt)
        self._check_collisions()

    def register_entity(self, entity: Entity) -> None:
        self._entities.append(entity)

    def unregister_entity(self, entity: Entity) -> None:
        self._entities.remove(entity)

    def _check_collisions(self) -> None:
        colliders = [e for e in self._entities if isinstance(e, Collider)]
        for i, a in enumerate(colliders):
            for b in colliders[i + 1:]:
                key = frozenset((id(a), id(b)))
                hit = a.overlaps(b)

                if hit and key not in self._contacts:
                    self._contacts.add(key)
                    a.on_collision(b)
                    b.on_collision(a)
                elif not hit and key in self._contacts:
                    self._contacts.discard(key)
                    a.on_collision_exit(b)
                    b.on_collision_exit(a)
