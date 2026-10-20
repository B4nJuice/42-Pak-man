from .amelioration import Amelioration
from .skills.speed_skill import SpeedSkill


class SpeedAmelioration(Amelioration):
    def __init__(self) -> None:
        super().__init__([SpeedSkill()])
