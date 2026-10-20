from enum import Enum


class AmeliorationRarity(Enum):
    COMMON = 0.5
    UNCOMMON = 0.7
    RARE = 0.84
    EPIC = 0.94
    LEGENDARY = 0.99
    MYTHIC = 1

    @classmethod
    def get_rarity(cls, value: float) -> 'AmeliorationRarity':
        for rarity in cls:
            if value <= rarity.value:
                return rarity
        return cls.MYTHIC

    def get_rarity_power(self) -> float:
        return (self.value + 0.5) ** 3
