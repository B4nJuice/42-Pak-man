from src.game.ameliorations.amelioration import Amelioration
from src.game.ameliorations.skills.luck_skill import LuckSkill


class LuckAmelioration(Amelioration):
    def __init__(self) -> None:
        self.init([LuckSkill()])
