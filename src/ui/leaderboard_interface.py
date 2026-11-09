from collections.abc import Callable, Iterator
from math import floor
from typing import TYPE_CHECKING

from src.app import App
from src.config.config_model import ConfigModel
from src.fonts import FontKey
from src.graphics import ButtonState, Color, Position
from src.graphics.super_meshes import AlignEnum, Button
from src.graphics.super_meshes.button import ButtonTextConfig
from src.graphics.super_meshes.font_sequence import FontSequence
from src.settings import ActionKey
from src.texture.texture_keys import TextureKeys

if TYPE_CHECKING:
    from src.game.game import Game

from src.core.displayable import SimpleDisplayable
from src.graphics.mesh_layer import MeshLayer
from src.ui.interface import Interface


class LeaderboardInterface(Interface):
    config: ConfigModel
    app: App
    game: 'Game'
    layer: MeshLayer

    table_entry: list[Button]
    hovered_entry: int
    hovered_button: Button | None

    def __init__(self, game: 'Game') -> None:
        super().__init__(game)
        self.game = game
        self.app = game._app
        self.layer = MeshLayer()

        screen_width = self.game._screen.width
        screen_height = self.game._screen.height
        config = self.game._config
        self.config = config
        size = self.game._app.size
        fonts = self.game._app.fonts

        self.layer.meshes.append(SimpleDisplayable(
            app=game._app,
            texture_key=TextureKeys.MAIN_BACKDROP.str(),
            position=Position(screen_width // 2, screen_height // 2),
            width=screen_width,
            height=screen_height
        ))

        align_left: float = size.get(160)

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
                        align_left + x_offset,
                        size.get(y_offset),
                    ),
                    align=AlignEnum.LEFT
                )

            yield make(
                'PAK-MAN / HALL OF FAME',
                FontKey.TITLE_SECONDARY_9,
                config.how_to_play_text_secondary,
                44 + 9
            )
            yield make(
                'LEADERBOARD',
                FontKey.TITLE_42,
                config.victory_text_accent,
                70 + 40
            )
            yield make(
                'The maze remembers the best. Make your run count.',
                FontKey.TEXT_13,
                config.how_to_play_text_secondary,
                128 + 15
            )

        self.layer.meshes.extend(_how_to_play_texts())

        self.layer.meshes.append(Button(
            position=Position(
                size.get(1016),
                size.get(92.5)
            ),
            width=size.get(104),
            height=size.get(36),
            normal_color=Color(*config.leaderboard_bg_secondary),
            border_color=Color(*config.leaderboard_border),
            border_thickness=size.get(1),
            on_click=self._exit,
            texts=[
                ButtonTextConfig(
                    text='ALL TIME',
                    font=fonts.get(FontKey.TITLE_SECONDARY_9),
                    color=Color(*config.leaderboard_text_accent),
                    offset_y=size.get(5),
                )
            ]
        ))

        self.table_entry = []
        self.hovered_entry = 3
        entry_y: float = size.get(219)
        w, h = size.get(960), size.get(46)
        x_text_pos: int = w // 2

        self.layer.meshes.append(Button(
            position=Position(
                align_left,
                entry_y - size.get(38)
            ),
            width=w,
            height=size.get(38),
            normal_color=Color(*config.leaderboard_bg_secondary),
            hover_color=Color(*config.leaderboard_bg_secondary),
            border_color=Color(*config.leaderboard_border),
            hover_border_color=Color(*config.leaderboard_border),
            border_thickness=size.get(1),
            texts=[
                ButtonTextConfig(
                    text='RANK',
                    font=fonts.get(FontKey.BOLD_10),
                    color=Color(*config.leaderboard_text_secondary),
                    offset_x=-x_text_pos + size.get(24),
                    offset_y=size.get(4),
                    alignment=AlignEnum.LEFT
                ),
                ButtonTextConfig(
                    text='PLAYER',
                    font=fonts.get(FontKey.BOLD_10),
                    color=Color(*config.how_to_play_text_secondary),
                    offset_x=-x_text_pos + size.get(108),
                    offset_y=size.get(4),
                    alignment=AlignEnum.LEFT
                ),
                ButtonTextConfig(
                    text='SCORE',
                    font=fonts.get(FontKey.BOLD_10),
                    color=Color(*config.how_to_play_text_secondary),
                    offset_x=x_text_pos - size.get(352),
                    offset_y=size.get(4),
                    alignment=AlignEnum.RIGHT
                ),
                ButtonTextConfig(
                    text='TIME',
                    font=fonts.get(FontKey.BOLD_10),
                    color=Color(*config.how_to_play_text_secondary),
                    offset_x=x_text_pos - size.get(232),
                    offset_y=size.get(4),
                    alignment=AlignEnum.RIGHT
                ),
                ButtonTextConfig(
                    text='RESULT',
                    font=fonts.get(FontKey.BOLD_10),
                    color=Color(*config.how_to_play_text_secondary),
                    offset_x=x_text_pos - size.get(24),
                    offset_y=size.get(4),
                    alignment=AlignEnum.RIGHT
                )
            ]
        ))
        for idx in range(8):
            button: Button = Button(
                position=Position(
                    align_left,
                    entry_y + (h + size.get(1)) * idx
                ),
                width=w,
                height=h,
                normal_color=Color(*config.leaderboard_bg),
                hover_color=Color(*config.leaderboard_bg_accent),
                border_color=Color(*config.leaderboard_border),
                hover_border_color=Color(*config.leaderboard_border_accent),
                border_thickness=size.get(1),
                on_hover=self._hover_callback(idx),
                texts=[
                    ButtonTextConfig(
                        text=f'{idx+1:02d}',
                        font=fonts.get(FontKey.TITLE_18),
                        color=Color(
                            *
                            config.leaderboard_text_accent
                            if idx == 0 else
                            config.leaderboard_text_secondary
                        ),
                        offset_x=-x_text_pos + size.get(24),
                        offset_y=size.get(7),
                        alignment=AlignEnum.LEFT,
                        state_colors={
                            ButtonState.HOVER: Color(
                                *config.how_to_play_text_accent
                            )
                        }
                    ),
                    ButtonTextConfig(
                        text='--',
                        font=fonts.get(FontKey.TITLE_SECONDARY_10),
                        color=Color(*config.how_to_play_text),
                        offset_x=-x_text_pos + size.get(108),
                        offset_y=size.get(7),
                        alignment=AlignEnum.LEFT,
                        state_colors={
                            ButtonState.HOVER: Color(
                                *config.how_to_play_text_accent
                            )
                        }
                    ),
                    ButtonTextConfig(
                        text='--',
                        font=fonts.get(FontKey.TITLE_18),
                        color=Color(*config.how_to_play_text),
                        offset_x=x_text_pos - size.get(352),
                        offset_y=size.get(7),
                        alignment=AlignEnum.RIGHT,
                        state_colors={
                            ButtonState.HOVER: Color(
                                *config.how_to_play_text_accent
                            )
                        }
                    ),
                    ButtonTextConfig(
                        text='--:--',
                        font=fonts.get(FontKey.BOLD_14),
                        color=Color(*config.how_to_play_text_secondary),
                        offset_x=x_text_pos - size.get(232),
                        offset_y=size.get(5),
                        alignment=AlignEnum.RIGHT
                    ),
                    ButtonTextConfig(
                        text='--',
                        font=fonts.get(FontKey.BOLD_12),
                        color=Color(*config.leaderboard_text_accent2),
                        offset_x=x_text_pos - size.get(24),
                        offset_y=size.get(5),
                        alignment=AlignEnum.RIGHT
                    )
                ]
            )
            self.table_entry.append(button)

            if idx == self.hovered_entry:
                self.hovered_button = button
                button.set_hovered(True)

        for entry in self.table_entry:
            self.layer.meshes.append(entry)

        self._update_entries()

        button_y: int = size.get(606)
        button_w: int = size.get(260)
        self.layer.meshes.append(Button(
            position=Position(
                align_left,
                button_y
            ),
            width=button_w,
            height=size.get(52),
            normal_color=Color(*config.leaderboard_bg_secondary),
            hover_color=Color(*config.leaderboard_bg_secondary),
            border_color=Color(*config.leaderboard_border),
            border_thickness=size.get(1),
            on_click=self._exit,
            texts=[
                ButtonTextConfig(
                    text='MAIN MENU',
                    font=fonts.get(FontKey.TITLE_18),
                    color=Color(*config.leaderboard_text),
                    alignment=AlignEnum.LEFT,
                    offset_y=size.get(6),
                    offset_x=-(button_w // 2) + size.get(18),
                ),
                ButtonTextConfig(
                    text='ESC',
                    font=fonts.get(FontKey.TITLE_SECONDARY_9),
                    color=Color(*config.leaderboard_text_secondary),
                    alignment=AlignEnum.RIGHT,
                    offset_x=(button_w // 2) - size.get(18),
                    offset_y=size.get(5),
                )
            ]
        ))

        self.layer.meshes.append(FontSequence(
            text='ARROW KEYS  MOVE   /   ENTER  SELECT',
            font=fonts.get(FontKey.TITLE_SECONDARY_9),
            color=Color(*config.leaderboard_text_secondary),
            position=Position(
                size.get(40),
                size.get(700.5)
            ),
            align=AlignEnum.LEFT
        ))
        self.layer.meshes.append(FontSequence(
            text='TOP 8 RUNS',
            font=fonts.get(FontKey.TITLE_SECONDARY_9),
            color=Color(*config.leaderboard_text_secondary),
            position=Position(
                screen_width - size.get(40),
                size.get(700.5)
            ),
            align=AlignEnum.RIGHT
        ))

    def display(self) -> None:
        self._update_entries()
        super().display()

    def handle_key(self, key: int) -> bool:
        if self.hidden:
            return False
        if key in self.game._app.key_manager.get_keys(
                ActionKey.BACK_PAUSE_RESUME
        ):
            self._exit()
            return True
        return False

    def _update_selection(self) -> None:
        for button in self.table_entry:
            button.set_hovered(
                button == self.table_entry[self.hovered_entry]
            )

    def _hover_callback(self, index: int) -> Callable[[], None]:
        def hover() -> None:
            self._hover_button(index)
            self.hovered_entry = index
            self._update_selection()
        return hover

    def _hover_button(self, index: int) -> None:
        if self.table_entry[index] is self.hovered_button:
            return

        self.hovered_button = self.table_entry[index]
        for button in self.table_entry:
            button.set_hovered(False)

    def _update_entries(self) -> None:
        for button, entry in zip(
                self.table_entry,
                self.app.leaderboard.get()[:len(self.table_entry)]
        ):
            button.texts[1].text = entry.name
            button.texts[2].text = f'{entry.score:,}'
            total_seconds = floor(entry.run_time)
            minutes, seconds = divmod(total_seconds, 60)
            button.texts[3].text = f'{minutes:02d}:{seconds:02d}'
            button.texts[4].text = 'VICTORY' if entry.victory else 'DEFEAT'
            button.texts[4].color = Color(
                *
                self.config.leaderboard_text_accent
                if entry.victory else
                self.config.leaderboard_text_accent2
            )
            button.refresh()

    def _exit(self) -> None:
        print('TODO: WARRNING !!!! : exit how to play interface')

    def get_layer(self) -> MeshLayer:
        return self.layer
