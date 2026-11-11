from typing import TYPE_CHECKING

from src.fonts import FontKey
from src.graphics import MeshLayer
from src.graphics.color import Color
from src.graphics.meshes.plane import Plane
from src.graphics.position import Position
from src.graphics.super_meshes import AlignEnum
from src.graphics.super_meshes.font_sequence import FontSequence
from src.ui.amelioration_interface import Rectangle
from src.ui.interface import Interface
from src.utils.size import SizeCore

if TYPE_CHECKING:
    from src.game import Game


class BoxInterface(Interface):
    layer: MeshLayer
    position: Position
    width: int
    height: int
    game: 'Game'
    background: Plane
    title: FontSequence
    value: str
    value_f: FontSequence

    def __init__(
                self,
                game: 'Game',
                title: str,
                value: str,
                position: Position,
                width: int,
                height: int,
                title_color: tuple[int, int, int],
                value_color: tuple[int, int, int],
                bg_color: tuple[int, int, int],
                border_color: tuple[int, int, int],
                title_fontkey: FontKey = FontKey.BOLD_10,
                value_fontkey: FontKey = FontKey.TITLE_22,
                title_font_size: float = 20,
                value_font_size: float = 22 + 27,
            ) -> None:
        """
        Initialize the instance.

        Args:
            game: Game instance associated with the component.
            title: Title used by the operation.
            value: Value to assign or apply.
            position: Screen or world coordinates of the object.
            width: Width of the screen or rendered element.
            height: Height of the screen or rendered element.
            title_color: Title color used by the operation.
            value_color: Value color used by the operation.
            bg_color: Bg color used by the operation.
            border_color: Border color used by the operation.
            title_fontkey: Title fontkey used by the operation.
            value_fontkey: Value fontkey used by the operation.
            title_font_size: Title font size used by the operation.
            value_font_size: Value font size used by the operation.
        """
        super().__init__(game)
        self.layer = MeshLayer()
        self.game = game
        size: SizeCore = self.game._app.size

        self.width = width
        self.height = height
        self.value = value
        self.background = Plane(
            Color(*bg_color),
            (
                position,
                Position(position.x + width, position.y + height)
            )
        )

        self.border = Rectangle(
            Color(*border_color),
            position,
            width,
            height,
            thickness=size.get(2),
            smooth_end=True
        )

        self.title = FontSequence(
            title,
            self.game._app.fonts.get(title_fontkey),
            Color(*title_color),
            Position(
                position.x + size.get(14),
                position.y + size.get(title_font_size)
            ),
            align=AlignEnum.LEFT
        )

        self.value_f = FontSequence(
            self.value,
            self.game._app.fonts.get(value_fontkey),
            Color(*value_color),
            Position(
                position.x + size.get(14),
                position.y + size.get(value_font_size)
            ),
            align=AlignEnum.LEFT,
        )

        self.layer.meshes.append(self.background)
        self.layer.meshes.append(self.border)
        self.layer.meshes.append(self.title)
        self.layer.meshes.append(self.value_f)

    def refresh(self, value: str) -> None:
        """
        Refresh the rendered state.

        Args:
            value: Value to assign or apply.
        """
        self.value = value
        self.value_f.set_sequence_text(self.value)

    def get_layer(self) -> MeshLayer:
        """
        Return the current layer.

        Returns:
            The current layer.
        """
        return self.layer
