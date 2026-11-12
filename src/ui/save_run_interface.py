from collections.abc import Iterator
from typing import TYPE_CHECKING

import pygame
from pydantic import ValidationError

from src.fonts import FontKey
from src.game.game_status import GameStatus
from src.graphics.super_meshes import (
    AlignEnum,
    Button,
    FontSequence,
)
from src.graphics.super_meshes.button import ButtonTextConfig
from src.leaderboard.leaderboard_models import MAX_ENTRIES, MAX_NAME_LENGTH
from src.utils import Logger, TColor

if TYPE_CHECKING:
    from src.game.game import Game

from src.graphics import Color, OperationEnum, Position
from src.graphics.mesh_layer import MeshLayer
from src.graphics.meshes import Plane

from .generators.popup_generator import generate_popup_bg
from .interface import Interface


class SaveRunInterface(Interface):
    logger: Logger
    game: 'Game'

    _score_buttons: Button
    _input: Button
    _input_value: str

    def __init__(self, game: 'Game') -> None:
        """
        Initialize the instance.

        Args:
            game: Game instance associated with the component.
        """
        self.logger = Logger(
            name='Cheat',
            color=TColor.BRIGHT_MAGENTA,
            verbose=game._logger.verbose
        )
        super().__init__(game)
        self.game = game
        self.layer = MeshLayer()

        screen_width = self.game._screen.width
        screen_height = self.game._screen.height
        config = self.game._config
        size = self.game._app.size
        fonts = self.game._app.fonts

        self.layer.meshes.append(Plane(
            Color(*config.cheat_overlay_color, 150),
            (
                Position(0, 0), Position(screen_width, screen_height)
            ),
            OperationEnum.ALPHA,
        ))

        width: int = 552
        height: int = 460

        popup_position, _, popup_plane, popup_border = \
            generate_popup_bg(
                width=width,
                height=height,
                bg_color=Color(*config.victory_bg),
                border_color=Color(*config.victory_border),
                border_tickness=2,
                screen_width=screen_width,
                screen_height=screen_height,
                size=size,
            )

        self.layer.meshes.append(popup_plane)
        self.layer.meshes.append(popup_border)

        align_left: float = popup_position.x + size.get(32)
        width_middle: float = screen_width / 2

        def _victory_texts() -> Iterator[FontSequence]:
            """
            Handle victory texts.

            Returns:
                The value produced by the victory texts operation.
            """
            def make(
                        text: str,
                        font_key: FontKey,
                        color: tuple[int, int, int],
                        y_offset: float,
                        x_offset: float = 0.0,
                        left: bool = True
                    ) -> FontSequence:
                """
                Handle make.

                Args:
                    text: Text used by the operation.
                    font_key: Font key used by the operation.
                    color: Color applied to the rendered element.
                    y_offset: Y offset used by the operation.
                    x_offset: X offset used by the operation.
                    left: Left used by the operation.

                Returns:
                    The value produced by the make operation.
                """
                return FontSequence(
                    text=text,
                    font=fonts.get(font_key),
                    color=Color(*color),
                    position=Position(
                        align_left
                        if left else
                        width_middle + size.get(x_offset),
                        popup_position.y + size.get(y_offset),
                    ),
                    align=AlignEnum.LEFT if left else AlignEnum.CENTER
                )

            yield make(
                'YOU MADE THE LEADERBOARD',
                FontKey.TITLE_SECONDARY_9,
                config.victory_text_accent,
                28 + 10
            )
            yield make(
                'CLAIM YOUR SPOT',
                FontKey.TITLE_30,
                config.victory_text,
                54 + 30
            )
            yield make(
                'Add your name to save this run to the leaderboard.',
                FontKey.TEXT_16,
                config.victory_text,
                98 + 16
            )
            yield make(
                'YOUR NAME (OPTIONAL)',
                FontKey.TITLE_SECONDARY_11,
                config.victory_text_secondary,
                208 + 11
            )
            yield make(
                'Leave blank to appear as “PAC RUNNER”.',
                FontKey.TEXT_14,
                config.victory_text_secondary,
                299 + 14
            )
            yield make(
                'USE “PAC-RUNNER” INSTEAD',
                FontKey.TITLE_SECONDARY_11,
                config.victory_text_secondary,
                404 + 11,
                left=False
            )

        self.layer.meshes.extend(_victory_texts())

        self._score_buttons = Button(
            position=Position(
                align_left,
                popup_position.y + size.get(134)
            ),
            width=size.get(488),
            height=size.get(52),
            normal_color=Color(*config.victory_bg_secondary),
            on_click=None,
            texts=[
                ButtonTextConfig(
                    text='#--',
                    font=fonts.get(FontKey.TITLE_18),
                    color=Color(*config.victory_text_accent),
                    alignment=AlignEnum.LEFT,
                    offset_y=size.get(6),
                    offset_x=-(size.get(488) // 2) + size.get(16),
                ),
                ButtonTextConfig(
                    text='-- PTS',
                    font=fonts.get(FontKey.TITLE_18),
                    color=Color(*config.victory_text),
                    alignment=AlignEnum.RIGHT,
                    offset_y=size.get(6),
                    offset_x=(size.get(488) // 2) - size.get(16),
                )
            ],
        )
        self.layer.meshes.append(self._score_buttons)

        self._input_value = ''
        self._input = Button(
            position=Position(
                align_left,
                popup_position.y + size.get(234)
            ),
            width=size.get(488),
            height=size.get(52),
            normal_color=Color(*config.victory_bg_accent2),
            border_color=Color(*config.victory_border_accent),
            border_thickness=size.get(1),
            on_click=None,
            texts=[
                ButtonTextConfig(
                    text='Enter your nickname',
                    font=fonts.get(FontKey.TEXT_17),
                    color=Color(*config.victory_text_secondary),
                    alignment=AlignEnum.LEFT,
                    offset_y=size.get(6),
                    offset_x=-(size.get(488) // 2) + size.get(16),
                )
            ],
        )
        self.layer.meshes.append(self._input)

        self.layer.meshes.append(Button(
            position=Position(
                align_left,
                popup_position.y + size.get(334)
            ),
            width=size.get(488),
            height=size.get(52),
            normal_color=Color(*config.victory_text_accent),
            border_color=Color(*config.victory_border_accent),
            border_thickness=size.get(1),
            on_click=self._submit,
            texts=[
                ButtonTextConfig(
                    text='CONTINUE',
                    font=fonts.get(FontKey.TITLE_18),
                    color=Color(*config.victory_bg),
                    alignment=AlignEnum.LEFT,
                    offset_y=size.get(6),
                    offset_x=-(size.get(488) // 2) + size.get(18),
                ),
                ButtonTextConfig(
                    text='ENTER',
                    font=fonts.get(FontKey.TITLE_SECONDARY_9),
                    color=Color(*config.victory_bg),
                    alignment=AlignEnum.RIGHT,
                    offset_x=(size.get(488) // 2) - size.get(18),
                    offset_y=size.get(5),
                )
            ],
        ))

    def display(self) -> None:
        """
        Display the interface contents.
        """
        score = self.game.get_score()
        rank = self.game._app.leaderboard.snapshot(score)
        self._update_score(
            rank if rank is not None else MAX_ENTRIES, score
        )

        return super().display()

    def _update_score(self, rank: int, score: int) -> None:
        """
        Handle update score.

        Args:
            rank: Rank used by the operation.
            score: Score to record or compare.
        """
        self._score_buttons.texts[0].text = f'#{rank+1:02d}'
        self._score_buttons.texts[1].text = f'{score:,} PTS'
        self._score_buttons.refresh()

    def _submit(self) -> None:
        """
        Handle submit.
        """
        score, run_time, _, _, _ = self.game.get_victory_values()
        try:
            self.game._app.leaderboard.add_run(
                name=self._input_value.upper().strip() or 'PAC RUNNER',
                run_time=run_time,
                score=score,
                victory=(self.game.get_status() == GameStatus.VICTORY)
            )
            self.game._interface_manager.back()
        except ValidationError as e:
            self.game._logger.pydantic_warning(e, prefix='Can\'t save run:')

    def _update_input(self) -> None:
        """
        Handle update input.
        """
        self._input.texts[0].text = (
            self._input_value.upper() or 'Enter your nickname'
        )
        self._input.refresh()

    def handle_key(self, key: int) -> bool:
        """
        Handle handle key.

        Args:
            key: Keyboard key code associated with the action.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        if self.hidden:
            return False

        if key == pygame.K_BACKSPACE:
            self._input_value = self._input_value[:-1]
        elif (
            pygame.K_a <= key <= pygame.K_z
            or pygame.K_0 <= key <= pygame.K_9
            or (key == pygame.K_SPACE and self._input_value)
        ) and len(self._input_value) < MAX_NAME_LENGTH:
            self._input_value += chr(key)
        elif key == pygame.K_RETURN:
            self._submit()

        self._update_input()
        return False

    def get_layer(self) -> MeshLayer:
        """
        Return the current layer.

        Returns:
            The current layer.
        """
        return self.layer
