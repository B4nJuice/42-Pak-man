from abc import ABC

from src.game import Game


class Interface(ABC):
    def __init__(self, game: Game) -> None:
        ...
