from typing import TYPE_CHECKING

from src.fonts import FontKey
from src.graphics import Color, Position
from src.graphics.super_meshes import AlignEnum
from src.graphics.super_meshes.font_sequence import FontSequence
from src.texture.texture_keys import TextureKeys

if TYPE_CHECKING:
    from src.game.game import Game

from src.core.displayable import SimpleDisplayable
from src.graphics.mesh_layer import MeshLayer
from src.ui.interface import Interface


class LobbyInterface(Interface):
    game: 'Game'
    layer: MeshLayer

    high_socre: FontSequence

    def __init__(self, game: 'Game') -> None:
        super().__init__(game)
        self.game = game
        self.layer = MeshLayer()

        screen_width = self.game._screen.width
        screen_height = self.game._screen.height
        config = self.game._config
        size = self.game._app.size
        fonts = self.game._app.fonts

        self.layer.meshes.append(SimpleDisplayable(
            app=game._app,
            texture_key=TextureKeys.MAIN_BACKDROP.str(),
            position=Position(screen_width // 2, screen_height // 2),
            width=screen_width,
            height=screen_height
        ))

        self.layer.meshes.append(FontSequence(
            text='HI-SCORE',
            font=fonts.get(FontKey.TITLE_SECONDARY_10),
            color=Color(*config.lobby_text_secondary),
            position=Position(
                size.get(440),
                size.get(64)
            ),
            align=AlignEnum.LEFT
        ))

        self.high_socre = FontSequence(
            text='048,620',
            font=fonts.get(FontKey.TITLE_SECONDARY_10),
            color=Color(*config.lobby_text_accent),
            position=Position(
                size.get(770),
                size.get(64)
            ),
            align=AlignEnum.LEFT
        )
        self.layer.meshes.append(self.high_socre)

        self.layer.meshes.append(FontSequence(
            text='PAK-MAN',
            font=fonts.get(FontKey.TITLE_88),
            color=Color(*config.lobby_text_accent),
            position=Position(
                screen_width // 2,
                size.get(122 + 88)
            ),
        ))
        self.layer.meshes.append(FontSequence(
            text='EAT. UPGRADE. SURVIVE.',
            font=fonts.get(FontKey.TITLE_SECONDARY_9),
            color=Color(*config.lobby_text_primary),
            position=Position(
                screen_width // 2,
                size.get(234 + 14)
            ),
        ))
        self.layer.meshes.append(FontSequence(
            text='Ten minutes. A whole lot of ghosts.',
            font=fonts.get(FontKey.TEXT_14),
            color=Color(*config.lobby_text_secondary),
            position=Position(
                screen_width // 2,
                size.get(264 + 9)
            ),
        ))

        w, h = (size.get(356), size.get(42))
        self.layer.meshes.append(SimpleDisplayable(
            app=game._app,
            texture_key=TextureKeys.LOBBY_ASSETS_PACMAN_GHOST,
            position=Position(
                size.get(462) + w / 2,
                size.get(292) + h / 2
            ),
            height=h,
            width=w
        ))

        self.layer.meshes.append(FontSequence(
            text='SURVIVE THE MAZE. BEAT THE SCORE.',
            font=fonts.get(FontKey.TITLE_SECONDARY_9),
            color=Color(*config.lobby_text_accent),
            position=Position(
                screen_width // 2,
                size.get(641 + 9)
            ),
        ))
        self.layer.meshes.append(FontSequence(
            text='ARROW KEYS  MOVE   /   ENTER  SELECT',
            font=fonts.get(FontKey.TITLE_SECONDARY_9),
            color=Color(*config.lobby_text_secondary),
            position=Position(
                size.get(40),
                size.get(700.5)
            ),
            align=AlignEnum.LEFT
        ))
        self.layer.meshes.append(FontSequence(
            text=f'V. {config.get_version()}',
            font=fonts.get(FontKey.TITLE_SECONDARY_9),
            color=Color(*config.lobby_text_secondary),
            position=Position(
                screen_width - size.get(40),
                size.get(700.5)
            ),
            align=AlignEnum.RIGHT
        ))


    def get_layer(self) -> MeshLayer:
        return self.layer
