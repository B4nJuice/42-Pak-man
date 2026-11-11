from collections.abc import Callable, Iterator
from typing import TYPE_CHECKING, Any

from src.core.displayable import SimpleDisplayable
from src.fonts import FontKey
from src.game.game_status import GameStatus, InterfaceStatus
from src.graphics.super_meshes import (
    AlignEnum,
    Button,
    ButtonState,
    FontSequence,
)
from src.graphics.super_meshes.button import ButtonTextConfig
from src.settings import ActionKey
from src.texture.texture_keys import TextureKeys
from src.utils import Logger, TColor

if TYPE_CHECKING:
    from src.game.game import Game

from src.graphics import Color, OperationEnum, Position
from src.graphics.mesh_layer import MeshLayer
from src.graphics.meshes import Plane

from .box_interface import BoxInterface
from .generators.popup_generator import generate_popup_bg
from .interface import Interface


class GameoverInterface(Interface):
    logger: Logger
    game: 'Game'
    prev_game_status: GameStatus
    layer: MeshLayer

    final_score: BoxInterface

    time_survived: BoxInterface
    level_reached: BoxInterface
    ghosts_defeated: BoxInterface
    pellets_eaten: BoxInterface

    def __init__(self, game: 'Game') -> None:
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

        width: int = 576
        height: int = 612

        popup_position, _, popup_plane, popup_border = \
            generate_popup_bg(
                width=width,
                height=height,
                bg_color=Color(*config.gameover_bg),
                border_color=Color(*config.gameover_border),
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
                        popup_position.y + size.get(y_offset),
                    ),
                )

            yield make(
                'NO LIVES REMAINING',
                FontKey.TITLE_SECONDARY_9,
                config.gameover_text_accent2,
                32 + 9
            )
            yield make(
                'GAME OVER',
                FontKey.TITLE_42,
                config.gameover_text,
                56 + 42,
                26
            )
            yield make(
                'The ghosts got you. Not the last word.',
                FontKey.TEXT_13,
                config.gameover_text,
                114 + 13
            )
            yield make(
                'ONE MORE RUN. YOU\'VE GOT THIS.',
                FontKey.TITLE_SECONDARY_9,
                config.gameover_text_secondary,
                546 + 9
            )

        self.layer.meshes.extend(_victory_texts())

        self.layer.meshes.append(SimpleDisplayable(
            app=game._app,
            texture_key=TextureKeys.GAMEOVER_GHOST,
            width=size.get(36),
            height=size.get(36),
            position=Position(
                popup_position.x + size.get(135 + 36 / 2),
                popup_position.y + size.get(64 + 36 / 2)
            )
        ))

        self.final_score = BoxInterface(
            game=game,
            title='FINAL SCORE',
            value='32,480',
            position=Position(
                align_left,
                popup_position.y + size.get(152)
            ),
            width=size.get(512),
            height=size.get(80),
            title_color=config.gameover_text_secondary,
            value_color=config.gameover_text_accent,
            bg_color=config.gameover_bg_secondary,
            border_color=config.gameover_border_secondary,
            value_fontkey=FontKey.TITLE_36,
            title_font_size=22.5,
            value_font_size=27.5 + 36
        )

        w, h = size.get(251), size.get(65)
        self.time_survived = BoxInterface(
            game=game,
            title='TIME SUVIVED',
            value='10:00',
            position=Position(
                align_left,
                popup_position.y + size.get(252)
            ),
            width=w,
            height=h,
            title_color=config.gameover_text_secondary,
            value_color=config.gameover_text,
            bg_color=config.gameover_bg_secondary,
            border_color=config.gameover_border_secondary,
        )
        self.level_reached = BoxInterface(
            game=game,
            title='LEVEL REACHED',
            value='24',
            position=Position(
                popup_position.x + size.get(293),
                popup_position.y + size.get(252)
            ),
            width=w,
            height=h,
            title_color=config.gameover_text_secondary,
            value_color=config.gameover_text,
            bg_color=config.gameover_bg_secondary,
            border_color=config.gameover_border_secondary,
        )
        self.ghosts_defeated = BoxInterface(
            game=game,
            title='GHOSTS DEFEATED',
            value='128',
            position=Position(
                align_left,
                popup_position.y + size.get(327)
            ),
            width=w,
            height=h,
            title_color=config.gameover_text_secondary,
            value_color=config.gameover_text,
            bg_color=config.gameover_bg_secondary,
            border_color=config.gameover_border_secondary,
        )
        self.pellets_eaten = BoxInterface(
            game=game,
            title='PELLETS EATEN',
            value='2,460',
            position=Position(
                popup_position.x + size.get(293),
                popup_position.y + size.get(327)
            ),
            width=w,
            height=h,
            title_color=config.gameover_text_secondary,
            value_color=config.gameover_text,
            bg_color=config.gameover_bg_secondary,
            border_color=config.gameover_border_secondary,
        )

        self.layer.meshes.append(self.final_score)
        self.layer.meshes.append(self.time_survived)
        self.layer.meshes.append(self.level_reached)
        self.layer.meshes.append(self.ghosts_defeated)
        self.layer.meshes.append(self.pellets_eaten)

        buttons_params: list[dict[str, Any]] = [
            {
                'label': 'PLAY AGAIN',
                'label_hover': '> PLAY AGAIN',
                'action_key_label': 'ENTER',
                'action': game.launch_new_run,
                'hover': self._hover_callback,
                'y': 412,
                'selected': True
            },
            {
                'label': 'MAIN MENU',
                'label_hover': '> MAIN MENU',
                'action_key_label': 'ESC',
                'action': lambda: self.game.set_interface_status(
                    InterfaceStatus.LOBBY
                ),
                'hover': self._hover_callback,
                'y': 474,
                'selected': False
            }
        ]
        self.buttons: list[Button] = []
        self.hovered_button: Button | None = None
        self._selected_index: int = 0

        for index, button_params in enumerate(buttons_params):
            button = Button(
                position=Position(
                    align_left,
                    popup_position.y + size.get(button_params['y'])
                ),
                width=size.get(512),
                height=size.get(52),
                normal_color=Color(*config.gameover_bg_secondary),
                hover_color=Color(*config.gameover_text_accent),
                border_color=Color(*config.gameover_border_secondary),
                hover_border_color=Color(*config.gameover_border_accent),
                border_thickness=size.get(1),
                on_click=button_params['action'],
                on_hover=button_params['hover'](index),
                texts=[
                    ButtonTextConfig(
                        text=button_params['label'],
                        font=fonts.get(FontKey.TITLE_18),
                        color=Color(*config.gameover_text),
                        alignment=AlignEnum.LEFT,
                        offset_y=size.get(6),
                        offset_x=-(size.get(512) // 2) + size.get(18),
                        state_colors={
                            ButtonState.HOVER: Color(
                                *config.gameover_bg
                            ),
                            ButtonState.SELECTED: Color(
                                *config.gameover_bg
                            ),
                        },
                        state_texts={
                            ButtonState.HOVER: button_params['label_hover'],
                            ButtonState.SELECTED: button_params['label_hover'],
                        }
                    ),
                    ButtonTextConfig(
                        text=button_params['action_key_label'],
                        font=fonts.get(FontKey.TITLE_SECONDARY_9),
                        color=Color(*config.gameover_text_secondary),
                        alignment=AlignEnum.RIGHT,
                        offset_x=(size.get(512) // 2) - size.get(18),
                        offset_y=size.get(5),
                        state_colors={
                            ButtonState.HOVER: Color(
                                *config.gameover_bg
                            ),
                            ButtonState.SELECTED: Color(
                                *config.gameover_bg
                            ),
                        },
                    )
                ],
            )
            if (button_params['selected']):
                button.set_selected(True)
            self.buttons.append(button)

        for button in self.buttons:
            self.layer.meshes.append(button)

    def update_values(
        self,
        final_score: int,
        time_survived: int,
        level_reached: int,
        ghosts_defeated: int,
        pellets_eaten: int,
    ) -> None:
        self.final_score.refresh(f'{final_score:,}')
        self.time_survived.refresh(
            f'{time_survived // 60:02}:{time_survived % 60:02}'
        )
        self.level_reached.refresh(f'{level_reached:,}')
        self.ghosts_defeated.refresh(f'{ghosts_defeated:,}')
        self.pellets_eaten.refresh(f'{pellets_eaten:,}')

    def display(self) -> None:
        self.update_values(*self.game.get_victory_values())
        super().display()

    def _update_selection(self) -> None:
        for button in self.buttons:
            button.set_selected(button == self.buttons[self._selected_index])

    def _hover_callback(self, index: int) -> Callable[[], None]:
        def hover() -> None:
            self._hover_button(index)
            self._selected_index = index
            self._update_selection()
        return hover

    def _hover_button(self, index: int) -> None:
        if self.buttons[index] is self.hovered_button:
            return

        self.hovered_button = self.buttons[index]
        for button in self.buttons:
            button.set_hovered(False)

    def handle_key(self, key: int) -> bool:
        if self.hidden:
            return False
        if key in self.game._app.key_manager.get_keys(
                    [
                        ActionKey.MOVE_LEFT,
                        ActionKey.MOVE_UP
                    ]
                ):
            self._selected_index = (
                    self._selected_index - 1
                ) % len(self.buttons)
            self._update_selection()
            return True
        if key in self.game._app.key_manager.get_keys(
                    [
                        ActionKey.MOVE_DOWN,
                        ActionKey.MOVE_RIGHT
                    ]
                ):
            self._selected_index = (
                    self._selected_index + 1
                ) % len(self.buttons)
            self._update_selection()
            return True
        if key in self.game._app.key_manager.get_keys(ActionKey.SELECT):
            self.buttons[self._selected_index].sim_click()
            return True
        if key in self.game._app.key_manager.get_keys(
            ActionKey.BACK_PAUSE_RESUME
        ):
            self.game.set_interface_status(InterfaceStatus.LOBBY)
            return True

        return False

    def get_layer(self) -> MeshLayer:
        return self.layer
