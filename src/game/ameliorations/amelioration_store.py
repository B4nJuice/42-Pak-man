from collections import defaultdict
from typing import TypeVar, cast

from src.errors import AmeliorationStoreNotFound
from .amelioration import Amelioration

A = TypeVar("A", bound=Amelioration)


class AmeliorationStore:
    _ameliorations: defaultdict[type[Amelioration], set[Amelioration]]

    def __init__(self) -> None:
        self._ameliorations = defaultdict(set)

    @staticmethod
    def _classes(amelioration: Amelioration) -> list[type[Amelioration]]:
        return [c for c in type(amelioration).__mro__ if issubclass(c, Amelioration)]

    def add(self, amelioration: Amelioration) -> None:
        for cls in self._classes(amelioration):
            self._ameliorations[cls].add(amelioration)

    def remove(self, amelioration: Amelioration) -> None:
        for cls in self._classes(amelioration):
            self._ameliorations[cls].discard(amelioration)

    def gets(self, cls: type[A]) -> list[A]:
        return cast(list[A], list(self._ameliorations.get(cls, ())))

    def get(self, cls: type[A]) -> A:
        ameliorations: list[A] = self.gets(cls)
        if (len(ameliorations) <= 0):
            raise AmeliorationStoreNotFound(str(cls))

        return cast(A, list(self._ameliorations.get(cls, ())).pop())

    def all(self) -> list[Amelioration]:
        return self.gets(Amelioration)

    def print(self) -> None:
        for key, value in self._ameliorations.items():
            print(f'{key.__name__}: {list(value)}')
