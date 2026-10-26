from typing import TYPE_CHECKING

from src.core.displayable import SimpleDisplayable
from src.game.ameliorations.amelioration import Amelioration
from src.graphics.color import Color
from src.graphics.mesh_layer import MeshLayer
from src.graphics.meshes.plane import Plane
from src.graphics.position import Position
from src.graphics.super_meshes import AlignEnum, FontSequence, Rectangle
from src.ui.interface import Interface
from src.utils.font_manager import FontKey
from src.utils.size import SizeCore

if TYPE_CHECKING:
    from src.game.game import Game


class AmeliorationCardInterface(Interface):
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
    size: SizeCore

    def __init__(
                self,
                game: 'Game',
                position: Position,
            ) -> None:
        self.layer = MeshLayer()
        self.position = position
        self.amelioration = None
        self.icon = None
        self.game = game
        self.size = self.game._app.size

        self.background = Plane(
            Color(*self.game._config.amelioration_card_color),
            (
                position,
                Position(
                    position.x + self.size.get(193),
                    position.y + self.size.get(289)
                )
            ),
            dynamic=False,
        )

        self.border = Rectangle(
            Color(*self.game._config.amelioration_card_border_color),
            position,
            self.size.get(193),
            self.size.get(289),
            thickness=2,
            smooth_end=True
        )

        self.amelioration_name = FontSequence(
            "",
            self.game._app.fonts.get(FontKey.TITLE_14),
            Color(*self.game._config.amelioration_name),
            Position(
                self.position.x + self.size.get(14),
                self.position.y + self.size.get(282),
            ),
            align=AlignEnum.LEFT,
            dynamic=True,
        )

        self.layer.meshes.append(self.background)
        self.layer.meshes.append(self.border)


    def set_amelioration(self, amelioration: Amelioration) -> None:
        self.amelioration = amelioration
        if self.icon is not None:
            self.layer.meshes.remove(self.icon)
        if self.amelioration_name in self.layer.meshes:
            self.layer.meshes.remove(self.amelioration_name)

        self.icon = SimpleDisplayable(
            self.game._app,
            self.amelioration.get_texture_key(),
            self.size.get(75),
            self.size.get(75),
            Position(
                self.position.x + self.size.get(95.5),
                self.position.y + self.size.get(94.5)
            ),

        )

        self.amelioration_name.set_sequence_text(
            amelioration.get_name().upper()
        )

        self.layer.meshes.append(self.amelioration_name)
        self.layer.meshes.append(self.icon)

    def get_layer(self) -> MeshLayer:
        return self.layer
