from collections.abc import Callable, Iterator
from typing import TYPE_CHECKING

from src.app import App
from src.fonts import FontKey
from src.graphics import Color, Mesh, Position
from src.graphics.meshes import Plane
from src.graphics.super_meshes import AlignEnum, Button, Rectangle
from src.graphics.super_meshes.button import ButtonTextConfig
from src.graphics.super_meshes.font_sequence import FontSequence
from src.settings import ActionKey
from src.texture.texture_keys import TextureKeys

if TYPE_CHECKING:
    from src.game.game import Game

from src.core.displayable import SimpleDisplayable
from src.graphics.mesh_layer import MeshLayer
from src.ui.interface import Interface


class SettingsInterface(Interface):
    app: App
    game: 'Game'
    layer: MeshLayer

    table_entry: list[Button]

    def __init__(self, game: 'Game') -> None:
        super().__init__(game)
        self.game = game
        self.app = game._app
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

        def _settings_texts() -> Iterator[FontSequence]:
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
                        screen_width / 2,
                        size.get(y_offset),
                    ),
                )

            yield make(
                'PAK-MAN / OPTIONS',
                FontKey.TITLE_SECONDARY_9,
                config.settings_text_secondary,
                44 + 9
            )
            yield make(
                'SETTINGS',
                FontKey.TITLE_42,
                config.settings_text_accent,
                70 + 40
            )
            yield make(
                'Your maze. Your rules. Fine-tune your next run.',
                FontKey.TEXT_13,
                config.settings_text_secondary,
                128 + 15
            )

        self.layer.meshes.extend(_settings_texts())

        def _settings_box() -> Iterator[tuple[Mesh, ...]]:
            def make(
                    x: float,
                    y: float,
                    w: float,
                    h: float,
                    title: str,
                    categorie: str
            ) -> tuple[Mesh, ...]:
                x = size.get(x)
                y = size.get(y)
                w = size.get(w)
                h = size.get(h)
                return (
                    Plane(
                        color=Color(*config.settings_bg),
                        positions=(
                            Position(
                                x,
                                y
                            ),
                            Position(
                                x + w,
                                y + h
                            )
                        )
                    ),
                    Rectangle(
                        color=Color(*config.settings_border),
                        position=Position(
                            x,
                            y
                        ),
                        width=w,
                        height=h,
                        thickness=size.get(1),
                    ),
                    # FontSequence(
                    # )
                )

            # yield

        def _settings_buttons() -> Iterator[Button]:
            def make(
                        w: float,
                        h: float,
                        x: float,
                        y: float,
                        cb: Callable,
                        txt: str,
                        key: str = '',
                        bg_color: tuple[int, int, int] =
                        config.settings_bg_secondary,
                        border_color: tuple[int, int, int] =
                        config.settings_border,
                        txt_color: tuple[int, int, int] =
                        config.settings_text,
                        key_color: tuple[int, int, int] =
                        config.settings_text_secondary

                    ) -> Button:
                return Button(
                    position=Position(
                        x,
                        y
                    ),
                    width=size.get(w),
                    height=size.get(h),
                    normal_color=Color(*bg_color),
                    hover_color=Color(*bg_color),
                    border_color=Color(*border_color),
                    border_thickness=size.get(1),
                    on_click=cb,
                    texts=[
                        ButtonTextConfig(
                            text=txt,
                            font=fonts.get(FontKey.TITLE_18),
                            color=Color(*txt_color),
                            alignment=AlignEnum.LEFT,
                            offset_y=size.get(6),
                            offset_x=size.get((-w / 2) + 18),
                        ),
                        ButtonTextConfig(
                            text=key,
                            font=fonts.get(FontKey.TITLE_SECONDARY_9),
                            color=Color(*key_color),
                            alignment=AlignEnum.RIGHT,
                            offset_x=size.get((w / 2) - 18),
                            offset_y=size.get(5),
                        )
                    ]
                )

            yield make(
                w=180,
                h=52,
                x=align_left,
                y=size.get(608),
                cb=self._exit,
                txt='Back',
                key='ESC'
            )

            yield make(
                w=272,
                h=52,
                x=size.get(312),
                y=size.get(608),
                cb=self._restore_default,
                txt='RESTORE DEFAULT',
                key=''
            )

            yield make(
                w=240,
                h=52,
                x=size.get(920),
                y=size.get(608),
                cb=self._apply,
                txt='> APPLY',
                key='ENTER',
                bg_color=config.settings_bg_accent,
                border_color=config.settings_border_accent,
                txt_color=config.settings_button_text_accent,
                key_color=config.settings_button_text_accent
            )

        self.layer.meshes.extend(_settings_buttons())

        self.layer.meshes.append(FontSequence(
            text='ARROW KEYS  MOVE   /   ENTER  SELECT   /   ESC  BACK',
            font=fonts.get(FontKey.TITLE_SECONDARY_9),
            color=Color(*config.settings_text_secondary),
            position=Position(
                size.get(40),
                size.get(700.5)
            ),
            align=AlignEnum.LEFT
        ))
        self.layer.meshes.append(FontSequence(
            text=f'V. {config.get_version()}',
            font=fonts.get(FontKey.TITLE_SECONDARY_9),
            color=Color(*config.settings_text_secondary),
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

    def _restore_default(self) -> None:
        print('TODO: WARRNING !!!! : exit how to play interface')

    def _apply(self) -> None:
        print('TODO: WARRNING !!!! : exit how to play interface')

    def get_layer(self) -> MeshLayer:
        return self.layer
