import sys
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from src.fonts.font_manager import FontKey
from src.graphics.meshes.line import Line
from src.graphics.super_meshes import AlignEnum, FontSequence
from src.settings.action_key import ActionKey

from ..graphics.super_meshes.button import (
    Button,
    ButtonState,
    ButtonTextConfig,
)

if TYPE_CHECKING:
    from src.game.game import Game

from src.game.game_status import GameStatus
from src.graphics import Color, OperationEnum, Position
from src.graphics.mesh_layer import MeshLayer
from src.graphics.meshes import Plane

from .generators.popup_generator import generate_popup_bg
from .interface import Interface


class EscapeInterface(Interface):
    def __init__(self, game: 'Game') -> None:
        super().__init__(game)
        self.game: Game = game
        self.hidden: bool = True
        self.layer: MeshLayer = MeshLayer()

        screen_width = self.game._screen.width
        screen_height = self.game._screen.height
        config = self.game._config
        size = self.game._app.size
        fonts = self.game._app.fonts

        self.background = Plane(
            Color(*config.pause_menu_overlay_color, 150),
            (
                Position(0, 0), Position(screen_width, screen_height)
            ),
            OperationEnum.ALPHA,
        )

        width: int = 520
        height: int = 465
        width_middle: int = screen_width // 2

        popup_position, _, popup_plane, popup_border = \
            generate_popup_bg(
                width=width,
                height=height,
                bg_color=Color(*config.pause_menu_background_color),
                border_color=Color(*config.pause_menu_border_color),
                border_tickness=2,
                screen_width=screen_width,
                screen_height=screen_height,
                size=size,
            )

        self.layer.meshes.append(self.background)
        self.layer.meshes.append(popup_plane)
        self.layer.meshes.append(popup_border)

        texts: list[FontSequence] = []
        texts.append(FontSequence(
            text='RUN ON HOLD',
            font=fonts.get(FontKey.TITLE_SECONDARY_9),
            color=Color(*config.pause_menu_text_secondary),
            position=Position(
                width_middle,
                popup_position.y + size.get(50)
            )
        ))
        texts.append(FontSequence(
            text='PAUSED',
            font=fonts.get(FontKey.TITLE_42),
            color=Color(*config.pause_menu_text_primary),
            position=Position(
                width_middle,
                popup_position.y + size.get(100)
            )
        ))

        texts.append(FontSequence(
            text='The maze can wait. Take a breather.',
            font=fonts.get(FontKey.TEXT_13),
            color=Color(*config.pause_menu_text_secondary),
            position=Position(
                width_middle,
                popup_position.y + size.get(128)
            )
        ))

        texts.append(FontSequence(
            text='Returning to the menu ends your current run.',
            font=fonts.get(FontKey.TEXT_12),
            color=Color(*config.pause_menu_text_secondary),
            position=Position(
                width_middle,
                popup_position.y + size.get(395)
            )
        ))

        texts.append(FontSequence(
            text='PRESS ESC TO RESUME',
            font=fonts.get(FontKey.TITLE_SECONDARY_9),
            color=Color(*config.pause_menu_text_button),
            position=Position(
                width_middle,
                popup_position.y + size.get(433)
            )
        ))

        for text in texts:
            self.layer.meshes.append(text)

        buttons_params: list[dict[str, Any]] = [
            {
                'label': 'RESUME',
                'label_hover': '> RESUME',
                'action_key_label': 'ESC',
                'action_key': None,
                'action': self.action_resume,
                'hover': self._hover_callback,
                'y': 153,
                'selected': True
            },
            {
                'label': 'SETTINGS',
                'label_hover': '> SETTINGS',
                'action_key_label': None,
                'action_key': None,
                'action': None,
                'hover': self._hover_callback,
                'y': 246,
                'selected': False
            },
            {
                'label': 'MAIN MENU',
                'label_hover': '> MAIN MENU',
                'action_key_label': None,
                'action_key': None,
                'action': self.action_main_menu,
                'hover': self._hover_callback,
                'y': 318,
                'selected': False
            }
        ]
        self.buttons: list[Button] = []
        self.hovered_button: Button | None = None
        self._selected_index: int = 0

        for index, button_params in enumerate(buttons_params):
            button = Button(
                position=Position(
                    popup_position.x + size.get(32),
                    popup_position.y + size.get(button_params['y'])
                ),
                width=size.get(456),
                height=size.get(52),
                normal_color=Color(*config.pause_menu_button_color),
                hover_color=Color(*config.pause_menu_button_hover_color),
                border_color=Color(*config.pause_menu_border_color),
                hover_border_color=Color(
                    *config.pause_menu_button_hover_color
                ),
                border_thickness=size.get(1),
                on_click=button_params['action'],
                on_hover=button_params['hover'](index),
                texts=[
                    ButtonTextConfig(
                        text=button_params['label'],
                        font=fonts.get(FontKey.TITLE_18),
                        color=Color(*config.pause_menu_text_button),
                        alignment=AlignEnum.LEFT,
                        offset_y=size.get(6),
                        offset_x=-(size.get(456) // 2) + size.get(18),
                        state_colors={
                            ButtonState.HOVER: Color(
                                *config.pause_menu_text_button_hover
                            ),
                            ButtonState.SELECTED: Color(
                                *config.pause_menu_text_button_hover
                            ),
                        },
                        state_texts={
                            ButtonState.HOVER: button_params['label_hover'],
                            ButtonState.SELECTED: button_params['label_hover'],
                        }
                    ),
                    *(
                        [
                            ButtonTextConfig(
                                text=button_params['action_key_label'],
                                font=fonts.get(FontKey.TITLE_SECONDARY_9),
                                color=Color(*config.pause_menu_text_button),
                                alignment=AlignEnum.RIGHT,
                                offset_x=(size.get(456) // 2) - size.get(18),
                                offset_y=size.get(5),
                                state_colors={
                                    ButtonState.HOVER: Color(
                                        *config.pause_menu_text_button_hover
                                    ),
                                    ButtonState.SELECTED: Color(
                                        *config.pause_menu_text_button_hover
                                    ),
                                },
                            )
                        ]
                        if button_params['action_key_label'] is not None
                        else []
                    ),
                ],
            )
            if (button_params['selected']):
                button.set_selected(True)
            self.buttons.append(button)

        for button in self.buttons:
            self.layer.meshes.append(button)

        line: Line = Line(
            color=Color(*config.pause_menu_border_color),
            start_position=Position(
                popup_position.x + size.get(32),
                popup_position.y + size.get(225)
            ),
            end_position=Position(
                popup_position.x + size.get(32 + 456),
                popup_position.y + size.get(225)
            ),
        )
        self.layer.meshes.append(line)
        self.hide()

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
        return False

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

    def hide(self) -> None:
        self.hidden = True

    def display(self) -> None:
        self.hidden = False

    def action_pause(self) -> None:
        self.display()
        self.game.set_status(GameStatus.PAUSED)

    def action_resume(self) -> None:
        self.hide()
        self.game.set_status(GameStatus.RUNNING)

    def action_main_menu(self) -> None:
        self.hide()
        print('To implement (Main Menu -> escape_interface.py)!')
        sys.exit(0)

    def get_layer(self) -> MeshLayer:
        return self.layer
