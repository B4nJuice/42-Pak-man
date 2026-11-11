from random import uniform

from ..amelioration_rarity import AmeliorationRarity
from .skill import Skill
from .skill_type import SkillType


class SuperTimeSkill(Skill):
    def __init__(self) -> None:
        """
        Initialize the instance.
        """
        super().__init__(SkillType.STATIC, default_value=0)
        self.set_name("Super time")
        self._suffix = "s"

    def next_upgrade(self, rarity: AmeliorationRarity) -> float:
        """
        Handle next upgrade.

        Args:
            rarity: Rarity used by the operation.

        Returns:
            The value produced by the next upgrade operation.
        """
        return 0.75 * rarity.get_rarity_power() * uniform(0.75, 1)
