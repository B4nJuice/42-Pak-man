from random import uniform

from src.game.ameliorations.amelioration_rarity import AmeliorationRarity
from src.game.ameliorations.skills.skill import Skill
from src.game.ameliorations.skills.skill_type import SkillType


class LuckSkill(Skill):
    def __init__(self) -> None:
        """
        Initialize the instance.
        """
        super().__init__(SkillType.PERCENTAGE, default_value=0)
        self.set_name("Luck")

    def next_upgrade(self, rarity: AmeliorationRarity) -> float:
        """
        Handle next upgrade.

        Args:
            rarity: Rarity used by the operation.

        Returns:
            The value produced by the next upgrade operation.
        """
        return 2 * rarity.get_rarity_power() * uniform(0.75, 1)
