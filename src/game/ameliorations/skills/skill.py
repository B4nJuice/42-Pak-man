from abc import ABC, abstractmethod

from src.game.ameliorations.amelioration_rarity import AmeliorationRarity
from src.game.ameliorations.skills.skill_type import SkillType


class Skill(ABC):
    _type: SkillType
    _value: float
    _suffix: str
    _name: str

    def __init__(
                self,
                skill_type: SkillType = SkillType.PERCENTAGE,
                default_value: float = 0
            ) -> None:
        """
        Initialize the instance.

        Args:
            skill_type: Skill type used by the operation.
            default_value: Default value used by the operation.
        """
        self._type = skill_type
        self._value = default_value
        self._suffix = "%"

    @abstractmethod
    def next_upgrade(self, rarity: AmeliorationRarity) -> float:
        """
        Handle next upgrade.

        Args:
            rarity: Rarity used by the operation.

        Returns:
            The value produced by the next upgrade operation.
        """
        pass

    def get_suffix(self) -> str:
        """
        Return the current suffix.

        Returns:
            The current suffix.
        """
        return self._suffix

    def set_name(self, name: str) -> None:
        """
        Assign the name.

        Args:
            name: Name assigned to the object or requested value.
        """
        self._name = name

    def get_name(self) -> str:
        """
        Return the current name.

        Returns:
            The current name.
        """
        return self._name

    def upgrade(self, value: float) -> None:
        """
        Handle upgrade.

        Args:
            value: Value to assign or apply.
        """
        self._value += value

    def get_type(self) -> SkillType:
        """
        Return the current type.

        Returns:
            The current type.
        """
        return self._type

    def get_value(self) -> float:
        """
        Return the current value.

        Returns:
            The current value.
        """
        return self._value
