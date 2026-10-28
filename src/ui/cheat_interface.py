from typing import TYPE_CHECKING, Any

from src.fonts.font_manager import FontKey
from src.graphics.meshes.line import Line
from src.graphics.super_meshes import (
    AlignEnum,
    FontSequence,
    ToggleButton,
    ToggleState,
    ToggleTextConfig,
)

from ..graphics.super_meshes.button import (
    Button,
    ButtonState,
    ButtonTextConfig,
)

if TYPE_CHECKING:
    from src.game.game import Game

from src.graphics import Color, OperationEnum, Position
from src.graphics.mesh_layer import MeshLayer
from src.graphics.meshes import Plane

from .generators.popup_generator import generate_popup_bg
from .interface import Interface


class CheatInterface(Interface):
    game: 'Game'
    layer: MeshLayer

    time_speed_active: float
    time_speed_buttons: dict[float, Button]

    def __init__(self, game: 'Game') -> None:
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
            dynamic=True,
        ))

        width: int = 856
        height: int = 648

        popup_position, popup_size, popup_plane, popup_border = \
            generate_popup_bg(
                width=width,
                height=height,
                bg_color=Color(*config.cheat_background_color),
                border_color=Color(*config.cheat_border_color),
                border_tickness=2,
                screen_width=screen_width,
                screen_height=screen_height,
                size=size,
            )

        self.layer.meshes.append(popup_plane)
        self.layer.meshes.append(popup_border)

        align_left: float = popup_position.x + size.get(32)
        align_right: float = popup_position.x + popup_size[0] - size.get(32)

        texts: list[FontSequence] = []
        texts.append(FontSequence(
            text='RUN MODIFIERS',
            font=fonts.get(FontKey.TITLE_SECONDARY_9),
            color=Color(*config.pause_menu_text_secondary),
            position=Position(
                align_left,
                popup_position.y + size.get(50)
            ),
            align=AlignEnum.LEFT
        ))
        texts.append(FontSequence(
            text='CHEATS',
            font=fonts.get(FontKey.TITLE_42),
            color=Color(*config.pause_menu_text_primary),
            position=Position(
                align_left,
                popup_position.y + size.get(100)
            ),
            align=AlignEnum.LEFT
        ))
        texts.append(FontSequence(
            text='2 cheats active',
            font=fonts.get(FontKey.TEXT_13),
            color=Color(*config.pause_menu_text_secondary),
            position=Position(
                align_right,
                popup_position.y + size.get(77.5 + 15)
            ),
            align=AlignEnum.RIGHT
        ))
        texts.append(FontSequence(
            text='Bend the rules. Changes affect this run only.',
            font=fonts.get(FontKey.TEXT_12),
            color=Color(*config.pause_menu_text_secondary),
            position=Position(
                align_left,
                popup_position.y + size.get(586.5 + 15)
            ),
            align=AlignEnum.LEFT
        ))

        for text in texts:
            self.layer.meshes.append(text)

        self.layer.meshes.append(Button(
            position=Position(
                popup_position.x + size.get(753),
                popup_position.y + size.get(32)
            ),
            width=size.get(71),
            height=size.get(30),
            normal_color=Color(*config.pause_menu_button_color),
            hover_color=Color(*config.pause_menu_button_hover_color),
            border_color=Color(*config.pause_menu_border_color),
            hover_border_color=Color(
                *config.pause_menu_button_hover_color
            ),
            border_thickness=size.get(1),
            on_click=self.action_close,
            texts=[
                ButtonTextConfig(
                    text='ESC',
                    font=fonts.get(FontKey.TITLE_SECONDARY_9),
                    color=Color(*config.pause_menu_text_button),
                    alignment=AlignEnum.LEFT,
                    offset_y=size.get(6),
                    offset_x=-(size.get(71) // 2) + size.get(10),
                    state_colors={
                        ButtonState.HOVER: Color(
                            *config.pause_menu_text_button_hover
                        ),
                        ButtonState.SELECTED: Color(
                            *config.pause_menu_text_button_hover
                        ),
                    },
                ),
                ButtonTextConfig(
                    text='X',
                    font=fonts.get(FontKey.BOLD_14),
                    color=Color(*config.pause_menu_text_button),
                    alignment=AlignEnum.RIGHT,
                    offset_y=size.get(6),
                    offset_x=(size.get(71) // 2) - size.get(10),
                ),
            ],
        ))

        toggles_params: list[dict[str, Any]] = [
            {
                'name': 'God Mod',
                'description': 'Take no damage',
                'action': self.toggle_godmod,
                'status': self.game.get_godmod_status(),
                'x': 0,
                'y': 0
            },
            {
                'name': 'No Clip',
                'description': 'Pass through walls',
                'action': self.toggle_noclip,
                'status': self.game.get_noclip_status(),
                'x': 1,
                'y': 0
            },
            {
                'name': 'Wall Hack',
                'description': 'Predicts ghost movements through walls',
                'action': self.toggle_wallhack,
                'status': self.game.get_wallhack_status(),
                'x': 0,
                'y': 1
            },
            {
                'name': 'Freeze Ghosts',
                'description': 'Pause ghost movement',
                'action': self.toggle_freeze,
                'status': self.game.get_freeze_status(),
                'x': 1,
                'y': 1
            }
        ]

        toggle_gap: int = size.get(12)
        toggle_width: int = size.get(390)
        toggle_height: int = size.get(68)
        toggle_x: float = popup_position.x + size.get(32)
        toggle_y: float = popup_position.y + size.get(116)

        for toggle_params in toggles_params:
            toggle: ToggleButton = ToggleButton(
                position=Position(
                    toggle_x + (toggle_width + toggle_gap)
                    * toggle_params['x'],
                    toggle_y + (toggle_height + toggle_gap)
                    * toggle_params['y']
                ),
                width=toggle_width,
                height=toggle_height,
                state=ToggleState.get(toggle_params['status']),
                inactive_color=Color(*config.cheat_toggle_bg_inactive_color),
                active_color=Color(*config.cheat_toggle_bg_active_color),
                inactive_track_color=Color(
                    *config.cheat_toggle_button_inactive_color
                ),
                active_track_color=Color(
                    *config.cheat_toggle_button_active_color
                ),
                thumb_inactive_color=Color(
                    *config.cheat_toggle_text_inactive_color
                ),
                thumb_active_color=Color(
                    *config.cheat_toggle_text_active_color
                ),
                border_color=Color(*config.cheat_toggle_border_color),
                border_thickness=2,
                operation=OperationEnum.ALPHA,
                switch_padding=size.get(12),
                switch_padding_inner=size.get(4),
                track_width=size.get(64),
                track_height=size.get(28),
                thumb_size=size.get(18),
                switch_side='right',
                texts=[
                    ToggleTextConfig(
                        text='',
                        font=fonts.get(FontKey.TITLE_SECONDARY_9),
                        color=Color(*config.cheat_toggle_text_inactive_color),
                        alignment=AlignEnum.LEFT,
                        offset_x=size.get(152),
                        offset_y=size.get(4),
                        inactive_text='OFF',
                    ),
                    ToggleTextConfig(
                        text='ON',
                        font=fonts.get(FontKey.TITLE_SECONDARY_9),
                        color=Color(*config.cheat_toggle_text_active_color),
                        alignment=AlignEnum.LEFT,
                        offset_x=size.get(123),
                        offset_y=size.get(4),
                        inactive_text='',
                    ),
                    ToggleTextConfig(
                        text=toggle_params['name'],
                        font=fonts.get(FontKey.TITLE_13),
                        color=Color(*config.cheat_toggle_text_color),
                        alignment=AlignEnum.LEFT,
                        offset_x=-(toggle_width // 2) + size.get(12),
                        offset_y=size.get(-6),
                    ),
                    ToggleTextConfig(
                        text=toggle_params['description'],
                        font=fonts.get(FontKey.TEXT_11),
                        color=Color(*config.cheat_toggle_text_secondary_color),
                        alignment=AlignEnum.LEFT,
                        offset_x=-(toggle_width // 2) + size.get(12),
                        offset_y=size.get(14),
                    )
                ],
                on_click=toggle_params['action']
            )
            self.layer.meshes.append(toggle)

        titles_params: list[dict[str, Any]] = [
            {
                'label': 'Add Lives',
                'x': 0,
                'y': 0
            },
            {
                'label': 'Add Xp',
                'x': 1,
                'y': 0
            },
            {
                'label': 'Add Timer',
                'x': 0,
                'y': 1
            },
            {
                'label': 'Time Speed',
                'x': 1,
                'y': 1
            },
            {
                'label': 'Change Level',
                'x': 0,
                'y': 2
            },
            {
                'label': 'Give Skills',
                'x': 1,
                'y': 2
            }
        ]

        title_gap_x: int = size.get(24)
        title_gap_y: int = size.get(20)
        title_width: int = size.get(384)
        title_height: int = size.get(62)
        title_x: float = popup_position.x + size.get(32)
        title_y: float = popup_position.y + size.get(305 + 8)

        for title_params in titles_params:
            self.layer.meshes.append(FontSequence(
                text=title_params['label'],
                font=fonts.get(FontKey.TITLE_14),
                color=Color(*config.cheat_text_color),
                position=Position(
                    title_x + (title_width + title_gap_x) * title_params['x'],
                    title_y + (title_height + title_gap_y) * title_params['y']
                ),
                align=AlignEnum.LEFT
            ))

        buttons_params: list[dict[str, Any]] = [
            {
                'type': 'label',
                'content': '3',
                'label': 'lives',
                'w': size.get(292),
                'h': size.get(36),
                'x': align_left,
                'y': popup_position.y + size.get(331),
                'action': None,
            },
            {
                'type': 'button',
                'content': '+ Add',
                'w': size.get(84),
                'h': size.get(36),
                'x': popup_position.x + size.get(332),
                'y': popup_position.y + size.get(331),
                'action': None,
            },

            {
                'type': 'button',
                'content': '- Remove',
                'w': size.get(120),
                'h': size.get(36),
                'x': align_left,
                'y': popup_position.y + size.get(413),
                'action': None,
            },
            {
                'type': 'label',
                'content': '60',
                'label': 'seconds',
                'w': size.get(128),
                'h': size.get(36),
                'x': popup_position.x + size.get(160),
                'y': popup_position.y + size.get(413),
                'action': None,
            },
            {
                'type': 'button',
                'content': '+ Add',
                'w': size.get(120),
                'h': size.get(36),
                'x': popup_position.x + size.get(296),
                'y': popup_position.y + size.get(413),
                'action': None,
            },

            {
                'type': 'button',
                'content': 'Prev Level',
                'w': size.get(120),
                'h': size.get(36),
                'x': align_left,
                'y': popup_position.y + size.get(495),
                'action': None,
            },
            {
                'type': 'label',
                'content': 'Level 01',
                'label': '',
                'w': size.get(128),
                'h': size.get(36),
                'x': popup_position.x + size.get(160),
                'y': popup_position.y + size.get(495),
                'action': None,
            },
            {
                'type': 'button',
                'content': 'Next Level',
                'w': size.get(120),
                'h': size.get(36),
                'x': popup_position.x + size.get(296),
                'y': popup_position.y + size.get(495),
                'action': None,
            },

            {
                'type': 'label',
                'content': '500',
                'label': 'xp',
                'w': size.get(292),
                'h': size.get(36),
                'x': popup_position.x + size.get(440),
                'y': popup_position.y + size.get(331),
                'action': None,
            },
            {
                'type': 'button',
                'content': '+ Add',
                'w': size.get(84),
                'h': size.get(36),
                'x': popup_position.x + size.get(740),
                'y': popup_position.y + size.get(331),
                'action': None,
            },

            {
                'type': 'button',
                'content': '↑',
                'w': size.get(36),
                'h': size.get(36),
                'x': popup_position.x + size.get(440),
                'y': popup_position.y + size.get(495),
                'action': None,
            },
            {
                'type': 'button',
                'content': '↓',
                'w': size.get(36),
                'h': size.get(36),
                'x': popup_position.x + size.get(696),
                'y': popup_position.y + size.get(495),
                'action': None,
            },
            {
                'type': 'button',
                'content': 'Give',
                'w': size.get(84),
                'h': size.get(36),
                'x': popup_position.x + size.get(740),
                'y': popup_position.y + size.get(495),
                'action': None,
            },
        ]

        for button_params in buttons_params:
            if button_params['type'] == 'label':
                self.layer.meshes.append(Button(
                    position=Position(
                        button_params['x'],
                        button_params['y']
                    ),
                    width=button_params['w'],
                    height=button_params['h'],
                    normal_color=Color(
                        *config.cheat_button_label_background_color
                    ),
                    hover_color=Color(
                        *config.cheat_button_label_background_color
                    ),
                    border_color=Color(
                        *config.cheat_button_label_border_color
                    ),
                    border_thickness=size.get(1),
                    on_click=button_params['action'],
                    texts=[
                        ButtonTextConfig(
                            text=button_params['content'],
                            font=fonts.get(FontKey.TITLE_SECONDARY_10),
                            color=Color(*config.cheat_button_label_text_color),
                            alignment=AlignEnum.LEFT,
                            offset_y=size.get(6),
                            offset_x=-(button_params['w'] // 2) + size.get(12),
                        ),
                        ButtonTextConfig(
                            text=button_params['label'],
                            font=fonts.get(FontKey.TEXT_12),
                            color=Color(
                                *config.cheat_button_label_text_secondary_color
                            ),
                            alignment=AlignEnum.RIGHT,
                            offset_y=size.get(4),
                            offset_x=(button_params['w'] // 2) - size.get(12),
                        ),
                    ]
                ))
            else:
                self.layer.meshes.append(Button(
                    position=Position(
                        button_params['x'],
                        button_params['y']
                    ),
                    width=button_params['w'],
                    height=button_params['h'],
                    normal_color=Color(
                        *config.cheat_button_action_background_color
                    ),
                    hover_color=Color(
                        *config.cheat_button_action_background_color
                    ),
                    border_color=Color(
                        *config.cheat_button_action_border_color
                    ),
                    border_thickness=size.get(1),
                    on_click=button_params['action'],
                    texts=[
                        ButtonTextConfig(
                            text=button_params['content'],
                            font=fonts.get(FontKey.TITLE_12),
                            color=Color(
                                *config.cheat_button_action_text_color
                            ),
                            offset_y=size.get(4),
                        ),
                    ]
                ))

        speed_button_gap: int = size.get(6)
        speed_button_width: int = size.get(91.5)
        speed_button_height: int = size.get(36)
        speed_button_x: float = popup_position.x + size.get(440)
        speed_button_y: float = popup_position.y + size.get(413)
        for idx, val in enumerate([0.5, 1, 2, 4]):
            self.layer.meshes.append(Button(
                position=Position(
                    speed_button_x + (speed_button_width + speed_button_gap) * idx,
                    speed_button_y
                ),
                width=speed_button_width,
                height=speed_button_height,
                normal_color=Color(
                    *config.cheat_button_label_background_color
                ),
                hover_color=Color(
                    *config.cheat_toggle_button_active_color, 18
                ),
                selected_color=Color(
                    *config.cheat_toggle_button_active_color, 18
                ),
                border_color=Color(
                    *config.cheat_button_label_border_color
                ),
                selected_border_color=Color(
                    *config.cheat_toggle_button_active_color
                ),
                border_thickness=size.get(1),
                on_click=None,
                state=ButtonState.SELECTED if val == 1 else ButtonState.NORMAL,
                texts=[
                    ButtonTextConfig(
                        text=f'{val}×',
                        font=fonts.get(FontKey.TITLE_SECONDARY_10),
                        color=Color(*config.cheat_button_label_text_color),
                        state_colors={
                            ButtonState.SELECTED: Color(
                                *config.cheat_toggle_button_active_color
                            )
                        },
                        offset_y=size.get(6),
                    )
                ]
            ))


        self.layer.meshes.append(Button(
            position=Position(
                popup_position.x + size.get(596),
                popup_position.y + size.get(572)
            ),
            width=size.get(228),
            height=size.get(44),
            normal_color=Color(*config.pause_menu_button_hover_color),
            hover_color=Color(*config.pause_menu_button_hover_color),
            border_color=Color(*config.pause_menu_button_hover_color),
            border_thickness=size.get(1),
            on_click=self.action_close,
            texts=[
                ButtonTextConfig(
                    text='> Back to game',
                    font=fonts.get(FontKey.TITLE_14),
                    color=Color(*config.pause_menu_text_button_hover),
                    alignment=AlignEnum.LEFT,
                    offset_y=size.get(6),
                    offset_x=-(size.get(228) // 2) + size.get(18),
                ),
                ButtonTextConfig(
                    text='ESC',
                    font=fonts.get(FontKey.TITLE_SECONDARY_8),
                    color=Color(*config.pause_menu_text_button_hover),
                    alignment=AlignEnum.RIGHT,
                    offset_x=(size.get(228) // 2) - size.get(18),
                    offset_y=size.get(5),
                )
            ],
        ))

        lines_params: list[int] = [284, 551]
        for line_params in lines_params:
            y: float = popup_position.y + size.get(line_params)
            self.layer.meshes.append(Line(
                color=Color(*config.pause_menu_border_color),
                start_position=Position(
                    popup_position.x + size.get(32),
                    y
                ),
                end_position=Position(
                    popup_position.x + size.get(width - 32),
                    y
                ),
            ))

        self.display()

    def add_life(self) -> None:
        print('add life')

    def add_xp(self) -> None:
        print('add xp')

    def add_timer(self) -> None:
        print('add timer')

    def remove_timer(self) -> None:
        print('remove timer')

    def prev_level(self) -> None:
        print('prev level')

    def next_level(self) -> None:
        print('next level')

    def set_time_speed(self) -> None:
        print('set time speed')

    def give_skill(self) -> None:
        print('give skill')

    def toggle_godmod(self, value: bool) -> None:
        self.game.toggle_godmod(value)

    def toggle_noclip(self, value: bool) -> None:
        print(f'toggle_noclip: {value}')
        self.game.toggle_noclip(value)

    def toggle_wallhack(self, value: bool) -> None:
        print(f'toggle_wallhack: {value}')
        self.game.toggle_wallhack(value)

    def toggle_freeze(self, value: bool) -> None:
        print(f'toggle_freeze: {value}')
        self.game.toggle_freeze(value)

    def hide(self) -> None:
        self.hidden = True

    def display(self) -> None:
        self.hidden = False

    def action_open(self) -> None:
        self.display()

    def action_close(self) -> None:
        self.hide()

    def get_layer(self) -> MeshLayer:
        return self.layer
