from collections import defaultdict
from typing import TypeVar, cast

from src.errors import EntityStoreNotFound

from .entity import Entity

E = TypeVar("E", bound=Entity)


class EntityStore:
    _entities: defaultdict[type[Entity], list[Entity]]

    def __init__(self) -> None:
        """
        Initialize the instance.
        """
        self._entities = defaultdict(list)

    @staticmethod
    def _classes(entity: Entity) -> list[type[Entity]]:
        """
        Handle classes.

        Args:
            entity: Entity used by the operation.

        Returns:
            The value produced by the classes operation.
        """
        return [c for c in type(entity).__mro__ if issubclass(c, Entity)]

    def add(self, entity: Entity) -> None:
        """
        Handle add.

        Args:
            entity: Entity used by the operation.
        """
        for cls in self._classes(entity):
            self._entities[cls].append(entity)

    def remove(self, entity: Entity) -> None:
        """
        Handle remove.

        Args:
            entity: Entity used by the operation.
        """
        for cls in self._classes(entity):
            self._entities[cls].remove(entity)

    def gets(self, cls: type[E]) -> list[E]:
        """
        Handle gets.

        Returns:
            The value produced by the gets operation.
        """
        return cast(list[E], list(self._entities.get(cls, ())))

    def get(self, cls: type[E]) -> E:
        """
        Handle get.

        Returns:
            The value produced by the get operation.
        """
        entities: list[E] = self.gets(cls)
        if (len(entities) <= 0):
            raise EntityStoreNotFound(str(cls))

        return cast(E, list(self._entities.get(cls, ())).pop())

    def all(self) -> list[Entity]:
        """
        Handle all.

        Returns:
            The value produced by the all operation.
        """
        return self.gets(Entity)

    def print(self) -> None:
        """
        Handle print.
        """
        for key, value in self._entities.items():
            print(f'{key.__name__}: {list(value)}')
