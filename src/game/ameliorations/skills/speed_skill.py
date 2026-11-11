from random import uniform

from ..amelioration_rarity import AmeliorationRarity
from .skill import Skill
from .skill_type import SkillType


class SpeedSkill(Skill):
    def __init__(self) -> None:
        """
        Initialize the instance.
        """
        super().__init__(SkillType.PERCENTAGE, default_value=0)
        self.set_name("Speed")

    def next_upgrade(self, rarity: AmeliorationRarity) -> float:
        """
        Handle next upgrade.

        Args:
            rarity: Rarity used by the operation.

        Returns:
            The value produced by the next upgrade operation.
        """
        return 3 * rarity.get_rarity_power() * uniform(0.75, 1)
