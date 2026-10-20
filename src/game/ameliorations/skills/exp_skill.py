from random import randint

from src.game.ameliorations.amelioration_rarity import AmeliorationRarity
from src.game.ameliorations.skills.skill import Skill
from src.game.ameliorations.skills.skill_type import SkillType


class ExpSkill(Skill):
    def __init__(self) -> None:
        super().__init__(SkillType.PERCENTAGE, default_value=0)

    def next_upgrade(self, rarity: AmeliorationRarity) -> float:
        return randint(2, 3) * rarity.get_rarity_power()
