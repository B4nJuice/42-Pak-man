from collections.abc import Iterator
from typing import TYPE_CHECKING

from src.fonts import FontKey
from src.graphics import Color, Position
from src.graphics.super_meshes import AlignEnum, Button
from src.graphics.super_meshes.button import ButtonTextConfig
from src.graphics.super_meshes.font_sequence import FontSequence
from src.settings import ActionKey
from src.texture.texture_keys import TextureKeys
from src.ui.how_to_play_section import HowToPlaySection

if TYPE_CHECKING:
    from src.game.game import Game

from src.core.displayable import SimpleDisplayable
from src.graphics.mesh_layer import MeshLayer
from src.ui.interface import Interface


class HowToPLayInterface(Interface):
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

        align_left: float = size.get(120)
        align_right: float = size.get(652)
        width_middle: float = screen_width / 2

        def _how_to_play_texts() -> Iterator[FontSequence]:
            def make(
                        text: str,
                        font_key: FontKey,
                        color: tuple[int, int, int],
                        y_offset: float,
                        x_offset: float = 0.0
                    ) -> FontSequence:
                return FontSequence(
                    text=text,
                    font=fonts.get(font_key),
                    color=Color(*color),
                    position=Position(
                        width_middle + size.get(x_offset),
                        size.get(y_offset),
                    ),
                )

            yield make(
                'PAK-MAN',
                FontKey.TITLE_SECONDARY_9,
                config.how_to_play_text_secondary,
                44 + 9
            )
            yield make(
                'HOW TO PLAY',
                FontKey.TITLE_42,
                config.victory_text_accent,
                70 + 40
            )
            yield make(
                'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
                FontKey.TEXT_13,
                config.how_to_play_text_secondary,
                128 + 15
            )

        self.layer.meshes.extend(_how_to_play_texts())

        # w, h = (size.get(356), size.get(42))
        # self.layer.meshes.append(SimpleDisplayable(
        #     app=game._app,
        #     texture_key=TextureKeys.LOBBY_ASSETS_PACMAN_GHOST,
        #     position=Position(
        #         size.get(462) + w / 2,
        #         size.get(292) + h / 2
        #     ),
        #     height=h,
        #     width=w
        # ))

        button_y: int = size.get(606)
        button_w: int = size.get(260)
        self.layer.meshes.append(Button(
            position=Position(
                align_left,
                button_y
            ),
            width=button_w,
            height=size.get(52),
            normal_color=Color(*config.how_to_play_button_bg),
            hover_color=Color(*config.how_to_play_button_bg),
            border_color=Color(*config.how_to_play_button_bg),
            border_thickness=size.get(1),
            on_click=self._exit,
            texts=[
                ButtonTextConfig(
                    text='< BACK',
                    font=fonts.get(FontKey.TITLE_18),
                    color=Color(*config.how_to_play_button_text),
                    alignment=AlignEnum.LEFT,
                    offset_y=size.get(6),
                    offset_x=-(button_w // 2) + size.get(18),
                ),
                ButtonTextConfig(
                    text='ESC',
                    font=fonts.get(FontKey.TITLE_SECONDARY_9),
                    color=Color(*config.how_to_play_button_text),
                    alignment=AlignEnum.RIGHT,
                    offset_x=(button_w // 2) - size.get(18),
                    offset_y=size.get(5),
                )
            ]
        ))

        sections_params: list[
            tuple[str, str, list[str], TextureKeys, float, float]
        ] = [
            (
                '01',
                'THE MAZE',
                [
                    'Lorem ipsum dolor sit amet, consectetur',
                    'adipiscing elit. Sed do eiusmod tempor',
                    'incididunt ut labore et dolore magna aliqua.'
                ],
                TextureKeys.HOW_TO_PLAY_01,
                align_left,
                size.get(178)
            ),
            (
                '02',
                'GHOSTS',
                [
                    'Ut enim ad minim veniam, quis nostrud',
                    'exercitation ullamco laboris nisi ut aliquip ex',
                    'ea commodo consequat.'
                ],
                TextureKeys.HOW_TO_PLAY_02,
                align_right,
                size.get(178)
            ),
            (
                '03',
                'SKILLS',
                [
                    'Duis aute irure dolor in reprehenderit in',
                    'voluptate velit esse cillum dolore eu fugiat',
                    'nulla pariatur.'
                ],
                TextureKeys.HOW_TO_PLAY_03,
                align_left,
                size.get(392)
            ),
            (
                '04',
                'STATS',
                [
                    'Excepteur sint occaecat cupidatat non',
                    'proident, sunt in culpa qui officia deserunt',
                    'mollit anim id est laborum.'
                ],
                TextureKeys.HOW_TO_PLAY_04,
                align_right,
                size.get(392)
            )
        ]

        for number, title, texts, texture_key, x, y in sections_params:
            self.layer.meshes.append(HowToPlaySection(
                game=game,
                position=Position(x, y),
                width=size.get(508),
                height=size.get(190),
                title=title,
                number=number,
                texts=texts,
                bg_color=config.how_to_play_bg,
                border_color=config.how_to_play_border,
                title_color=config.how_to_play_text,
                text_color=config.how_to_play_text_secondary,
                text_accent_color=config.how_to_play_text_accent,
                image_key=texture_key
            ))

        self.layer.meshes.append(FontSequence(
            text='ESC - BACK TO MENU',
            font=fonts.get(FontKey.TITLE_SECONDARY_9),
            color=Color(*config.how_to_play_text_secondary),
            position=Position(
                size.get(40),
                size.get(700.5)
            ),
            align=AlignEnum.LEFT
        ))
        self.layer.meshes.append(FontSequence(
            text=f'V. {config.get_version()}',
            font=fonts.get(FontKey.TITLE_SECONDARY_9),
            color=Color(*config.how_to_play_text_secondary),
            position=Position(
                screen_width - size.get(40),
                size.get(700.5)
            ),
            align=AlignEnum.RIGHT
        ))

    def handle_key(self, key: int) -> bool:
        if self.hidden:
            return False
        if key in self.game._app.key_manager.get_keys(
                ActionKey.BACK_PAUSE_RESUME
        ):
            self._exit()
            return True
        return False

    def _exit(self) -> None:
        print('TODO: WARRNING !!!! : exit how to play interface')

    def get_layer(self) -> MeshLayer:
        return self.layer
