from src.game.ameliorations.amelioration import Amelioration
from src.game.ameliorations.skills.exp_skill import ExpSkill


class ExpAmelioration(Amelioration):
    def __init__(self) -> None:
        self.init([ExpSkill()])
