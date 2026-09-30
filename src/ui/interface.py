from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.game.game import Game
from src.graphics.mesh_layer import MeshLayer


class Interface(ABC):
    def __init__(self, game: 'Game') -> None:
        ...

    @abstractmethod
    def get_layer(self) -> MeshLayer:
        ...
