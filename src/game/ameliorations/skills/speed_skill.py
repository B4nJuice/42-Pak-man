from random import randint

from src.game.ameliorations import Skill
from src.game.ameliorations import SkillType
from src.game.ameliorations import AmeliorationRarity

class SpeedSkill(Skill):
    def __init__(self) -> None:
        super().__init__(SkillType.PERCENTAGE, default_value = 0)

    def next_upgrade(self, rarity: AmeliorationRarity) -> float:
        return randint(2, 7) * rarity.value * 2
