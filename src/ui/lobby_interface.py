from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from src.fonts import FontKey
from src.game.game_status import InterfaceStatus
from src.graphics import Color, Position
from src.graphics.super_meshes import AlignEnum, Button, ButtonState
from src.graphics.super_meshes.button import ButtonTextConfig
from src.graphics.super_meshes.font_sequence import FontSequence
from src.settings import ActionKey
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
            text='---,---',
            font=fonts.get(FontKey.TITLE_SECONDARY_10),
            color=Color(*config.lobby_text_accent),
            position=Position(
                size.get(770),
                size.get(64)
            ),
            align=AlignEnum.LEFT
        )
        self._update_max_score()
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

        buttons_params: list[dict[str, Any]] = [
            {
                'label': 'START RUN',
                'label_hover': '> START RUN',
                'action_key_label': 'ENTER',
                'action_key': None,
                'action': game.launch_new_run,
                'hover': self._hover_callback,
                'y': 371,
                'selected': True
            },
            {
                'label': 'LEADERBOARD',
                'label_hover': '> LEADERBOARD',
                'action_key_label': None,
                'action_key': None,
                'action': lambda: self.game.set_interface_status(
                    InterfaceStatus.LEADERBOARD
                ),
                'hover': self._hover_callback,
                'y': 433,
                'selected': False
            },
            {
                'label': 'SETTINGS',
                'label_hover': '> SETTINGS',
                'action_key_label': None,
                'action_key': None,
                'action': lambda: self.game.set_interface_status(
                    InterfaceStatus.SETTINGS
                ),
                'hover': self._hover_callback,
                'y': 495,
                'selected': False
            },
            {
                'label': 'QUIT GAME',
                'label_hover': '> QUIT GAME',
                'action_key_label': None,
                'action_key': None,
                'action': game.exit,
                'hover': self._hover_callback,
                'y': 557,
                'selected': False
            }
        ]
        self.buttons: list[Button] = []
        self.hovered_button: Button | None = None
        self._selected_index: int = 0

        for index, button_params in enumerate(buttons_params):
            button = Button(
                position=Position(
                    size.get(450),
                    size.get(button_params['y'])
                ),
                width=size.get(380),
                height=size.get(52),
                normal_color=Color(*config.lobby_button_bg),
                hover_color=Color(*config.lobby_button_bg_accent),
                border_color=Color(*config.lobby_button_border),
                hover_border_color=Color(*config.lobby_button_border_accent),
                border_thickness=size.get(1),
                on_click=button_params['action'],
                on_hover=button_params['hover'](index),
                texts=[
                    ButtonTextConfig(
                        text=button_params['label'],
                        font=fonts.get(FontKey.TITLE_18),
                        color=Color(*config.lobby_button_text),
                        alignment=AlignEnum.LEFT,
                        offset_y=size.get(6),
                        offset_x=-(size.get(380) // 2) + size.get(18),
                        state_colors={
                            ButtonState.HOVER: Color(
                                *config.lobby_button_text_accent
                            ),
                            ButtonState.SELECTED: Color(
                                *config.lobby_button_text_accent
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
                                color=Color(*config.lobby_button_text),
                                alignment=AlignEnum.RIGHT,
                                offset_x=(size.get(380) // 2) - size.get(18),
                                offset_y=size.get(5),
                                state_colors={
                                    ButtonState.HOVER: Color(
                                        *config.lobby_button_text_accent
                                    ),
                                    ButtonState.SELECTED: Color(
                                        *config.lobby_button_text_accent
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

    def _update_max_score(self) -> None:
        self.high_socre.set_sequence_text(
            f'{self.game._app.leaderboard.get_max_score():07,d}'
        )

    def _update_selection(self) -> None:
        for button in self.buttons:
            button.set_selected(button == self.buttons[self._selected_index])

    def _hover_callback(self, index: int) -> Callable[[], None]:
        def hover() -> None:
            self._hover_button(index)
            self._selected_index = index
            self._update_selection()
        return hover

    def display(self) -> None:
        self._update_max_score()
        return super().display()

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
        return False

    def get_layer(self) -> MeshLayer:
        return self.layer
