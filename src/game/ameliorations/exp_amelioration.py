from src.game.ameliorations import Amelioration
from src.game.ameliorations import ExpSkill


class ExpAmelioration(Amelioration):
    def __init__(self) -> None:
        super().__init__([ExpSkill()])
