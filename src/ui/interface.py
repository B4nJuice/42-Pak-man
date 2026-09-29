from src.game import Game
from abc import ABC


class Interface(ABC):
    def __init__(self, game: Game) -> None:
        ...
