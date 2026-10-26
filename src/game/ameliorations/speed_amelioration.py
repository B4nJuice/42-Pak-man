from .amelioration import Amelioration
from .skills.speed_skill import SpeedSkill


class SpeedAmelioration(Amelioration):
    def __init__(self) -> None:
        self.init([SpeedSkill()], "amelioration-speed")
        self.set_name("Speed Ring")
        self.set_description("Move faster.")
