from abc import ABC
from typing import TYPE_CHECKING
import random

if TYPE_CHECKING:
    from src.game.ameliorations import AmeliorationRarity
    from src.game.ameliorations import Skill
    from src.game.ameliorations import SkillStore


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

    def next_upgrade(self) -> list[tuple['Skill', float]]:
        from src.game.ameliorations import AmeliorationRarity
        value: float = random.random()
        rarity: AmeliorationRarity = AmeliorationRarity.get_rarity(value)

        skills_upgrades: list[tuple['Skill', float]] = []

        for skill in self._skills:
            skills_upgrades.append((skill, skill.next_upgrade(rarity)))

        return skills_upgrades

    def level_up(self, value: float, rarity: 'AmeliorationRarity') -> None:
        self._level += 1

    def get_skills(self) -> list['Skill']:
        return self._skills.all()

    def get_skill(self, _type: type) -> 'Skill':
        return self._skills.get(_type)
