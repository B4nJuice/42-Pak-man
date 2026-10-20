from random import randint

from src.game.ameliorations import AmeliorationRarity, Skill, SkillType


class SpeedSkill(Skill):
    def __init__(self) -> None:
        super().__init__(SkillType.PERCENTAGE, default_value = 0)

    def next_upgrade(self, rarity: AmeliorationRarity) -> float:
        return randint(2, 5) * rarity.get_rarity_power()
