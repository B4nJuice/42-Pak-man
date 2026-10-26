from abc import ABC, abstractmethod

from src.game.ameliorations.amelioration_rarity import AmeliorationRarity
from src.game.ameliorations.skills.skill_type import SkillType


class Skill(ABC):
    _type: SkillType
    _value: float
    _suffix: str

    def __init__(
                self,
                skill_type: SkillType = SkillType.PERCENTAGE,
                default_value: float = 0
            ) -> None:
        self._type = skill_type
        self._value = default_value
        self._suffix = ""

    @abstractmethod
    def next_upgrade(self, rarity: AmeliorationRarity) -> float:
        pass

    def upgrade(self, value: float) -> None:
        self._value += value

    def get_type(self) -> SkillType:
        return self._type

    def get_value(self) -> float:
        return self._value
