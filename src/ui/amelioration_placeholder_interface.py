from typing import TYPE_CHECKING

from src.core.displayable import SimpleDisplayable
from src.game.ameliorations.amelioration import Amelioration
from src.graphics import OperationEnum
from src.graphics.color import Color
from src.graphics.mesh_layer import MeshLayer
from src.graphics.meshes.plane import Plane
from src.graphics.position import Position
from src.graphics.super_meshes import AlignEnum, FontSequence
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
    icon: SimpleDisplayable | None
    level: FontSequence
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
        self.icon = None
        self.game = game

        self.background = Plane(
            Color(*self.game._config.placeholder_amelioration_color),
            (
                position,
                Position(position.x + width, position.y + height)
            ),
            dynamic=False,
            operation=OperationEnum.ALPHA
        )

        self.layer.meshes.append(self.background)
        self.level = FontSequence(
            "",
            self.game._font,
            Color(*self.game._config.menu_text_color),
            Position(
                self.position.x + self.width - 4,
                self.position.y + self.height - 4,
            ),
            spacing=1,
            align=AlignEnum.RIGHT,
            dynamic=True,
        )
        self.level.set_scale(0.5)

    def set_amelioration(self, amelioration: Amelioration) -> None:
        self.amelioration = amelioration
        if self.icon is not None:
            self.layer.meshes.remove(self.icon)
        if self.level in self.layer.meshes:
            self.layer.meshes.remove(self.level)

        self.icon = SimpleDisplayable(
            self.game._app,
            self.amelioration.get_texture_key(),
            self.width,
            self.height,
            Position(
                self.position.x + self.width // 2,
                self.position.y + self.height // 2
            )
        )
        self.layer.meshes.append(self.icon)
        self.level.set_sequence_text(
            f"Lvl {self.amelioration.get_level()}"
        )
        self.layer.meshes.append(self.level)


    def get_layer(self) -> MeshLayer:
        return self.layer
