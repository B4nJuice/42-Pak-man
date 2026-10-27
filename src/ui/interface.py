from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from src.graphics.mesh_layer import MeshLayer

if TYPE_CHECKING:
    from src.game.game import Game


class Interface(ABC):
    hidden: bool

    def __init__(self, game: 'Game') -> None:
        self.hidden = False

    def is_hidden(self) -> bool:
        return self.hidden

    @abstractmethod
    def get_layer(self) -> MeshLayer:
        ...
