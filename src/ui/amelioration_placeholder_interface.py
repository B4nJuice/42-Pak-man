from typing import TYPE_CHECKING

from src.core.displayable import SimpleDisplayable
from src.fonts import FontKey
from src.game.ameliorations.amelioration import Amelioration
from src.graphics import OperationEnum
from src.graphics.color import Color
from src.graphics.mesh_layer import MeshLayer
from src.graphics.meshes.plane import Plane
from src.graphics.position import Position
from src.graphics.super_meshes import AlignEnum, FontSequence, Rectangle
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
    border: Rectangle
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
        super().__init__(game)

        self.background = Plane(
            Color(*self.game._config.placeholder_amelioration_color),
            (
                position,
                Position(position.x + width, position.y + height)
            ),
            dynamic=False,
            operation=OperationEnum.ALPHA
        )

        self.border = Rectangle(
            Color(*self.game._config.placeholder_amelioration_border_color),
            position,
            width,
            height,
            thickness=2,
            smooth_end=True
        )

        self.layer.meshes.append(self.background)
        self.layer.meshes.append(self.border)
        self.level = FontSequence(
            "",
            self.game._app.fonts.get(FontKey.TITLE_10),
            Color(*self.game._config.pause_menu_text_button),
            Position(
                self.position.x + self.width - self.game._app.size.get(3),
                self.position.y + self.height - self.game._app.size.get(3),
            ),
            align=AlignEnum.RIGHT,
            dynamic=True,
        )

    def set_amelioration(self, amelioration: Amelioration) -> None:
        self.amelioration = amelioration
        if self.icon is not None:
            self.layer.meshes.remove(self.icon)
        if self.level in self.layer.meshes:
            self.layer.meshes.remove(self.level)

        self.icon = SimpleDisplayable(
            self.game._app,
            self.amelioration.get_texture_key(),
            round(self.width * 0.72),
            round(self.height * 0.72),
            Position(
                self.position.x + self.width // 2,
                self.position.y + self.height // 2
            ),

        )
        self.layer.meshes.append(self.icon)
        self.level.set_sequence_text(
            f"LV.{self.amelioration.get_level()}"
        )
        self.layer.meshes.append(self.level)

    def get_layer(self) -> MeshLayer:
        return self.layer
