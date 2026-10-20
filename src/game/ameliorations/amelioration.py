import random
from abc import ABC
from typing import TYPE_CHECKING

from src.game.ameliorations.amelioration_rarity import AmeliorationRarity

if TYPE_CHECKING:
    from src.game.ameliorations import Skill, SkillStore


class Amelioration(ABC):
    _level: int
    _skills: 'SkillStore'

    def __init__(self, skills: list['Skill']) -> None:
        from src.game.ameliorations import SkillStore
        self._skills = SkillStore()
        for skill in skills:
            self._skills.add(skill)
        self._level = 0

    def get_level(self) -> int:
        return self._level

    def next_upgrade(self, luck: float = 1) -> tuple[
                AmeliorationRarity, list[tuple['Skill', float]]
            ]:
        from src.game.ameliorations import AmeliorationRarity
        value: float = random.random() * luck
        rarity: AmeliorationRarity = AmeliorationRarity.get_rarity(value)

        skills_upgrades: list[tuple[Skill, float]] = []

        for skill in self.get_skills():
            skills_upgrades.append((skill, skill.next_upgrade(rarity)))

        return (rarity, skills_upgrades)

    def level_up(self, skill_upgrades: list[tuple['Skill', float]]) -> None:
        self._level += 1
        for skill, value in skill_upgrades:
            skill.upgrade(value)

    def get_skills(self) -> list['Skill']:
        return self._skills.all()

    def get_skill(self, _type: type) -> 'Skill':
        return self._skills.get(_type)
