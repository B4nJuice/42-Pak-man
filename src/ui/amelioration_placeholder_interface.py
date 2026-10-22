from typing import TYPE_CHECKING

from src.core.displayable import SimpleDisplayable
from src.game.ameliorations.amelioration import Amelioration
from src.graphics.color import Color
from src.graphics.mesh_layer import MeshLayer
from src.graphics.meshes.plane import Plane
from src.graphics.position import Position
from src.ui.interface import Interface

if TYPE_CHECKING:
    from src.game.game import Game


class AmeliorationPlaceholderInterface(Interface):
    layer: MeshLayer
    position: Position
    width: int
    height: int
    amelioration: Amelioration | None
    background: Plane
    game: 'Game'

    def __init__(
                self,
                game: 'Game',
                position: Position,
                width: int,
                height: int
            ) -> None:
        self.layer = MeshLayer()
        self.position = position
        self.width = width
        self.height = height
        self.amelioration = None
        self.game = game

        self.background = Plane(
            Color(*self.game._config.placeholder_amelioration_color),
            (
                position,
                Position(position.x + width, position.y + height)
            ),
            dynamic=False
        )

        self.layer.meshes.append(self.background)

    def set_amelioration(self, amelioration: Amelioration) -> None:
        self.amelioration = amelioration
        SimpleDisplayable(
            self.game._app,
            self.amelioration.get_texture_key(),
            self.width,
            self.height,
            Position(
                self.position.x + self.width // 2,
                self.position.y + self.height // 2
            )
        )


    def get_layer(self) -> MeshLayer:
        return self.layer
