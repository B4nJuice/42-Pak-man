from src.game.ameliorations import Amelioration
from src.game.ameliorations import AmeliorationRarity
from src.game.ameliorations import SpeedSkill

class SpeedAmelioration(Amelioration):
    def __init__(self) -> None:
        super().__init__([SpeedSkill()])

    def level_up(self, value: float, rarity: AmeliorationRarity) -> None:
        super().level_up(value, rarity)
