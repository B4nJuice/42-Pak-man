from abc import ABC, abstractmethod

from src.game.ameliorations import SkillType
from src.game.ameliorations import AmeliorationRarity


class Skill(ABC):
    _type: SkillType
    _value: float

    def __init__(
                self,
                type: SkillType,
                default_value: float = 0
            ) -> None:
        self._type = type,
        self._value = 0

    @abstractmethod
    def next_upgrade(self, rarity: AmeliorationRarity) -> float:
        pass

    def upgrade(self, value: float) -> None:
        self._value += value

    def get_type(self) -> SkillType:
        return self._type

    def get_value(self) -> float:
        return self._value
