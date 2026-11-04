from typing import TYPE_CHECKING

from src.core.displayable import SimpleDisplayable
from src.fonts import FontKey
from src.graphics import MeshLayer
from src.graphics.color import Color
from src.graphics.meshes.plane import Plane
from src.graphics.position import Position
from src.graphics.super_meshes import AlignEnum
from src.graphics.super_meshes.font_sequence import FontSequence
from src.texture.texture_keys import TextureKeys
from src.ui.amelioration_interface import Rectangle
from src.ui.interface import Interface
from src.utils.size import SizeCore

if TYPE_CHECKING:
    from src.game import Game


class HowToPlaySection(Interface):
    layer: MeshLayer
    position: Position
    width: int
    height: int

    image: SimpleDisplayable

    title: FontSequence
    number: FontSequence
    texts: list[FontSequence]

    def __init__(
                self,
                game: 'Game',

                position: Position,
                width: int,
                height: int,

                title: str,
                number: str,
                texts: list[str],

                bg_color: tuple[int, int, int],
                border_color: tuple[int, int, int],
                title_color: tuple[int, int, int],
                text_color: tuple[int, int, int],
                text_accent_color: tuple[int, int, int],
                image_key: TextureKeys,
            ) -> None:
        super().__init__(game)
        self.layer = MeshLayer()
        self.game = game
        size: SizeCore = self.game._app.size

        self.width = width
        self.height = height

        self.layer.meshes.append(Plane(
            Color(*bg_color),
            (
                position,
                Position(position.x + width, position.y + height)
            )
        ))

        self.layer.meshes.append(Rectangle(
            Color(*border_color),
            position,
            width,
            height,
            thickness=size.get(1),
            smooth_end=True
        ))

        w, h = size.get(112), size.get(122)
        self.image = SimpleDisplayable(
            app=game._app,
            width=w,
            height=h,
            position=Position(
                position.x + size.get(24) + w / 2,
                position.y + size.get(34) + h / 2
            ),
            texture_key=image_key
        )

        self.number = FontSequence(
            number,
            self.game._app.fonts.get(FontKey.TITLE_SECONDARY_10),
            Color(*text_accent_color),
            Position(
                position.x + size.get(160),
                position.y + size.get(44.5 + 10)
            ),
            align=AlignEnum.LEFT,
        )

        self.title = FontSequence(
            title,
            self.game._app.fonts.get(FontKey.TITLE_SECONDARY_10),
            Color(*title_color),
            Position(
                position.x + size.get(192),
                position.y + size.get(44.5 + 10)
            ),
            align=AlignEnum.LEFT
        )

        self.texts = []
        text_x: float = position.x + size.get(160)
        text_y: float = position.y + size.get(76.5 + 15)
        text_gap: float = size.get(23)
        for idx, text in enumerate(texts):
            self.texts.append(FontSequence(
                text,
                self.game._app.fonts.get(FontKey.TEXT_15),
                Color(*text_color),
                Position(
                    text_x,
                    text_y + text_gap * idx
                ),
                align=AlignEnum.LEFT,
            ))

        self.layer.meshes.append(self.image)
        self.layer.meshes.append(self.number)
        self.layer.meshes.append(self.title)

        for text in self.texts:
            self.layer.meshes.append(text)

    def refresh(self) -> None:
        pass

    def get_layer(self) -> MeshLayer:
        return self.layer
