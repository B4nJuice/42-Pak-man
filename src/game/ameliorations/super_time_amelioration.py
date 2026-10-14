from src.game.ameliorations import Amelioration
from src.game.ameliorations import SuperTimeSkill


class SuperTimeAmelioration(Amelioration):
    def __init__(self) -> None:
        super().__init__([SuperTimeSkill()])
