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
        """
        Initialize the instance.
        """
        self._ameliorations = defaultdict(set)

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

    def add(self, amelioration: Amelioration) -> None:
        """
        Handle add.

        Args:
            amelioration: Amelioration used by the operation.
        """
        for skill in amelioration.get_skills():
            for cls in self._classes(skill):
                self._ameliorations[cls].add(amelioration)

    def remove(self, amelioration: Amelioration) -> None:
        """
        Handle remove.

        Args:
            amelioration: Amelioration used by the operation.
        """
        for skill in amelioration.get_skills():
            for cls in self._classes(skill):
                self._ameliorations[cls].discard(amelioration)

    def gets(self, cls: type[Skill]) -> list[Amelioration]:
        """
        Handle gets.

        Returns:
            The value produced by the gets operation.
        """
        return list(self._ameliorations.get(cls, ()))

    def get(self, cls: type[Skill]) -> Amelioration:
        """
        Handle get.

        Returns:
            The value produced by the get operation.
        """
        ameliorations: list[Amelioration] = self.gets(cls)
        if (len(ameliorations) <= 0):
            raise AmeliorationStoreNotFound(str(cls))

        return cast(Amelioration, list(self._ameliorations.get(cls, ())).pop())

    def get_by_type(
                self,
                amelioration: type[Amelioration]
            ) -> Amelioration | None:
        """
        Return the current by type.

        Args:
            amelioration: Amelioration used by the operation.

        Returns:
            The current by type.
        """
        gets = [
            a for a in self.all() if isinstance(a, amelioration)
        ]
        if len(gets) <= 0:
            return None
        else:
            return gets[0]

    def all(self) -> list[Amelioration]:
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
        for key, value in self._ameliorations.items():
            print(f'{key.__name__}: {list(value)}')
