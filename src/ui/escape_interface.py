from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.game.game import Game

from src.graphics import Color, Position, OperationEnum
from src.graphics.mesh_layer import MeshLayer
from src.graphics.super_meshes import Rectangle
from src.graphics.meshes import Plane
from src.ui import Interface


class EscapeInterface(Interface):
    def __init__(self, game : 'Game') -> None:
        self.game: Game = game
        self.hidden: bool = True
        self.layer: MeshLayer = MeshLayer()

        self.background = Plane(
            Color(0, 0, 0, 100),
            (
                Position(0, 0),
                Position(self.game._screen.width, self.game._screen.height)
            ),
            OperationEnum.ALPHA,
            dynamic=True
        )

        self.layer.meshes.append(self.background)
        self.hide()

    def hide(self) -> None:
        self.hidden = True
        for mesh in self.get_layer().meshes:
            mesh.set_hidden(True)

    def display(self) -> None:
        self.hidden = False
        for mesh in self.get_layer().meshes:
            mesh.set_hidden(False)

    def get_layer(self) -> MeshLayer:
        return self.layer
