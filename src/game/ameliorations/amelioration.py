from abc import ABC
from random import random
from typing import TYPE_CHECKING

from src.app import App
from src.core.displayable import SimpleDisplayable
from src.game.ameliorations.amelioration_rarity import AmeliorationRarity
from src.texture.animation_player import AnimationPlayer

if TYPE_CHECKING:
    from src.game.ameliorations import Skill, SkillStore


class Amelioration(SimpleDisplayable, ABC):
    _level: int
    _skills: 'SkillStore'
    _app: App
    _name: str
    _animation: AnimationPlayer
    _description: str

    def init(self, skills: list['Skill'], texture_key: str) -> None:
        """
        Initialize the associated state.

        Args:
            skills: Skills used by the operation.
            texture_key: Texture key used by the operation.
        """
        from src.game.ameliorations import SkillStore
        self._skills = SkillStore()
        for skill in skills:
            self._skills.add(skill)
        self._level = 0
        self.set_texture_key(texture_key)
        self.set_name(self.__class__.__name__.removesuffix("Amelioration"))

    def get_app(self) -> App:
        """
        Return the current app.

        Returns:
            The current app.
        """
        return self._app

    def set_description(self, description: str) -> None:
        """
        Assign the description.

        Args:
            description: Description used by the operation.
        """
        self._description = description

    def get_description(self) -> str:
        """
        Return the current description.

        Returns:
            The current description.
        """
        return self._description

    def set_name(self, name: str) -> None:
        """
        Assign the name.

        Args:
            name: Name assigned to the object or requested value.
        """
        self._name = name

    def get_name(self) -> str:
        """
        Return the current name.

        Returns:
            The current name.
        """
        return self._name

    def get_level(self) -> int:
        """
        Return the current level.

        Returns:
            The current level.
        """
        return self._level

    def next_upgrade(
                self,
                luck: float = 1,
                power: float = 0
            ) -> tuple[
                AmeliorationRarity, list[tuple['Skill', float]]
            ]:
        """
        Handle next upgrade.

        Args:
            luck: Luck used by the operation.
            power: Power used by the operation.

        Returns:
            The value produced by the next upgrade operation.
        """
        from src.game.ameliorations import AmeliorationRarity
        luck = max(luck, 1)
        value: float = random() ** (1 / luck)
        rarity: AmeliorationRarity = AmeliorationRarity.get_rarity(value)

        skills_upgrades: list[tuple[Skill, float]] = []

        for skill in self.get_skills():
            upgrade = skill.next_upgrade(rarity)
            skills_upgrades.append((skill, upgrade * (1 + power / 100)))

        return (rarity, skills_upgrades)

    def level_up(self, skill_upgrades: list[tuple['Skill', float]]) -> None:
        """
        Handle level up.

        Args:
            skill_upgrades: Skill upgrades used by the operation.
        """
        self._level += 1
        for skill, value in skill_upgrades:
            skill.upgrade(value)

    def get_skills(self) -> list['Skill']:
        """
        Return the current skills.

        Returns:
            The current skills.
        """
        return self._skills.all()

    def get_skill(self, _type: type) -> 'Skill':
        """
        Return the current skill.

        Args:
            _type: Type used by the operation.

        Returns:
            The current skill.
        """
        return self._skills.get(_type)
