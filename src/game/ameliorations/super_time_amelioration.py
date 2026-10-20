from .amelioration import Amelioration
from .skills.super_time_skill import SuperTimeSkill


class SuperTimeAmelioration(Amelioration):
    def __init__(self) -> None:
        super().__init__([SuperTimeSkill()])
