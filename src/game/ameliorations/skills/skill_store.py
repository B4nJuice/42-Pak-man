from collections import defaultdict
from typing import TypeVar, cast

from src.errors import SkillStoreNotFound
from .skill import Skill

A = TypeVar("A", bound=Skill)


class SkillStore:
    _skills: defaultdict[type[Skill], set[Skill]]

    def __init__(self) -> None:
        """
        Initialize the instance.
        """
        self._skills = defaultdict(set)

    @staticmethod
    def _classes(skill: Skill) -> list[type[Skill]]:
        """
        Handle classes.

        Args:
            skill: Skill used by the operation.

        Returns:
            The value produced by the classes operation.
        """
        return [c for c in type(skill).__mro__ if issubclass(c, Skill)]

    def add(self, skill: Skill) -> None:
        """
        Handle add.

        Args:
            skill: Skill used by the operation.
        """
        for cls in self._classes(skill):
            self._skills[cls].add(skill)

    def remove(self, skill: Skill) -> None:
        """
        Handle remove.

        Args:
            skill: Skill used by the operation.
        """
        for cls in self._classes(skill):
            self._skills[cls].discard(skill)

    def gets(self, cls: type[A]) -> list[A]:
        """
        Handle gets.

        Returns:
            The value produced by the gets operation.
        """
        return cast(list[A], list(self._skills.get(cls, ())))

    def get(self, cls: type[A]) -> A:
        """
        Handle get.

        Returns:
            The value produced by the get operation.
        """
        skills: list[A] = self.gets(cls)
        if (len(skills) <= 0):
            raise SkillStoreNotFound(str(cls))

        return cast(A, list(self._skills.get(cls, ())).pop())

    def all(self) -> list[Skill]:
        """
        Handle all.

        Returns:
            The value produced by the all operation.
        """
        return self.gets(Skill)

    def print(self) -> None:
        """
        Handle print.
        """
        for key, value in self._skills.items():
            print(f'{key.__name__}: {list(value)}')
