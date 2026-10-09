from collections import defaultdict
from typing import TypeVar, cast

from src.errors import EntityStoreNotFound

from .entity import Entity

E = TypeVar("E", bound=Entity)


class EntityStore:
    _entities: defaultdict[type[Entity], set[Entity]]

    def __init__(self) -> None:
        self._entities = defaultdict(set)

    @staticmethod
    def _classes(entity: Entity) -> list[type[Entity]]:
        return [c for c in type(entity).__mro__ if issubclass(c, Entity)]

    def add(self, entity: Entity) -> None:
        for cls in self._classes(entity):
            self._entities[cls].add(entity)

    def remove(self, entity: Entity) -> None:
        for cls in self._classes(entity):
            self._entities[cls].discard(entity)

    def gets(self, cls: type[E]) -> list[E]:
        return cast(list[E], list(self._entities.get(cls, ())))

    def get(self, cls: type[E]) -> E:
        entities: list[E] = self.gets(cls)
        if (len(entities) <= 0):
            raise EntityStoreNotFound(str(cls))

        return cast(E, list(self._entities.get(cls, ())).pop())

    def all(self) -> list[Entity]:
        return self.gets(Entity)

    def print(self) -> None:
        for key, value in self._entities.items():
            print(f'{key.__name__}: {list(value)}')
