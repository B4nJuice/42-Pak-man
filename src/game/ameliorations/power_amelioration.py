from src.game.ameliorations.amelioration import Amelioration
from src.game.ameliorations.skills.power_skill import PowerSkill


class PowerAmelioration(Amelioration):
    def __init__(self) -> None:
        self.init([PowerSkill()])
