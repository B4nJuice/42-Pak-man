from src.game.ameliorations.amelioration import Amelioration
from src.game.ameliorations.skills.luck_skill import LuckSkill


class LuckAmelioration(Amelioration):
    def __init__(self) -> None:
        """
        Initialize the instance.
        """
        self.init([LuckSkill()], "amelioration-luck")
        self.set_name("Luck Ring")
        self.set_description("Find better amelioration.")
