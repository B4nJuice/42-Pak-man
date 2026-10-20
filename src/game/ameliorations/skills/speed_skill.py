from random import uniform

from src.game.ameliorations import AmeliorationRarity, Skill, SkillType


class SpeedSkill(Skill):
    def __init__(self) -> None:
        super().__init__(SkillType.PERCENTAGE, default_value=0)

    def next_upgrade(self, rarity: AmeliorationRarity) -> float:
        return 3 * rarity.get_rarity_power() * uniform(0.75, 1)
