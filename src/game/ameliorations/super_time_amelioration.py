from .amelioration import Amelioration
from .skills.super_time_skill import SuperTimeSkill


class SuperTimeAmelioration(Amelioration):
    def __init__(self) -> None:
        """
        Initialize the instance.
        """
        self.init([SuperTimeSkill()], "amelioration-super-time")
        self.set_name("SuperTime Ring")
        self.set_description("Add super time.")
