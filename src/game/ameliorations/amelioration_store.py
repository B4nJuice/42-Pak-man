from collections import defaultdict
from typing import TypeVar, cast

from src.errors import AmeliorationStoreNotFound
from src.game.ameliorations.amelioration import Amelioration
from src.game.ameliorations.skills.skill import Skill

A = TypeVar("A", bound=Amelioration)
S = TypeVar("S", bound=Skill)


class AmeliorationStore:
    _ameliorations: defaultdict[type[Skill], set[Amelioration]]

    def __init__(self) -> None:
        self._ameliorations = defaultdict(set)

    @staticmethod
    def _classes(skill: Skill) -> list[type[Skill]]:
        return [c for c in type(skill).__mro__ if issubclass(c, Skill)]

    def add(self, amelioration: Amelioration) -> None:
        for skill in amelioration.get_skills():
            for cls in self._classes(skill):
                self._ameliorations[cls].add(amelioration)

    def remove(self, amelioration: Amelioration) -> None:
        for skill in amelioration.get_skills():
            for cls in self._classes(skill):
                self._ameliorations[cls].discard(amelioration)

    def gets(self, cls: type[Skill]) -> list[Amelioration]:
        return list(self._ameliorations.get(cls, ()))

    def get(self, cls: type[Skill]) -> Amelioration:
        ameliorations: list[Amelioration] = self.gets(cls)
        if (len(ameliorations) <= 0):
            raise AmeliorationStoreNotFound(str(cls))

        return cast(Amelioration, list(self._ameliorations.get(cls, ())).pop())

    def get_by_type(
                self,
                amelioration: type[Amelioration]
            ) -> Amelioration | None:
        gets =  [
            a for a in self.all() if isinstance(a, amelioration)
        ]
        if len(gets) <= 0:
            return None
        else:
            return gets[0]

    def all(self) -> list[Amelioration]:
        return self.gets(Skill)

    def print(self) -> None:
        for key, value in self._ameliorations.items():
            print(f'{key.__name__}: {list(value)}')
