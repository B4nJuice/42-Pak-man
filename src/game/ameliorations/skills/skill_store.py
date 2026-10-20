from collections import defaultdict
from typing import TypeVar, cast

from src.errors import SkillStoreNotFound
from .skill import Skill

A = TypeVar("A", bound=Skill)


class SkillStore:
    _skill: defaultdict[type[Skill], set[Skill]]

    def __init__(self) -> None:
        self._skills = defaultdict(set)

    @staticmethod
    def _classes(skill: Skill) -> list[type[Skill]]:
        return [c for c in type(skill).__mro__ if issubclass(c, Skill)]

    def add(self, skill: Skill) -> None:
        for cls in self._classes(skill):
            self._skills[cls].add(skill)

    def remove(self, skill: Skill) -> None:
        for cls in self._classes(skill):
            self._skills[cls].discard(skill)

    def gets(self, cls: type[A]) -> list[A]:
        return cast(list[A], list(self._skills.get(cls, ())))

    def get(self, cls: type[A]) -> A:
        skills: list[A] = self.gets(cls)
        if (len(skills) <= 0):
            raise SkillStoreNotFound(str(cls))

        return cast(A, list(self._skills.get(cls, ())).pop())

    def all(self) -> list[Skill]:
        return self.gets(Skill)

    def print(self) -> None:
        for key, value in self._skills.items():
            print(f'{key.__name__}: {list(value)}')
