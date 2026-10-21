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

    def init(self, skills: list['Skill'], texture_key: str) -> None:
        from src.game.ameliorations import SkillStore
        self._skills = SkillStore()
        for skill in skills:
            self._skills.add(skill)
        self._level = 0
        self.set_texture_key(texture_key)
        self.set_name(self.__class__.__name__.removesuffix("Amelioration"))

    def get_app(self) -> App:
        return self._app

    def set_name(self, name: str) -> None:
        self._name = name

    def get_name(self) -> str:
        return self._name

    def get_level(self) -> int:
        return self._level

    def next_upgrade(
                self,
                luck: float = 1,
                power: float = 0
            ) -> tuple[
                AmeliorationRarity, list[tuple['Skill', float]]
            ]:
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
        self._level += 1
        for skill, value in skill_upgrades:
            skill.upgrade(value)

    def get_skills(self) -> list['Skill']:
        return self._skills.all()

    def get_skill(self, _type: type) -> 'Skill':
        return self._skills.get(_type)
