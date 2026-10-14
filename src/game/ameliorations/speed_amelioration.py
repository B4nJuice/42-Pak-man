from src.game.ameliorations import Amelioration
from src.game.ameliorations import SpeedSkill

class SpeedAmelioration(Amelioration):
    def __init__(self) -> None:
        super().__init__([SpeedSkill()])
