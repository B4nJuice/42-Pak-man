from typing import TYPE_CHECKING

from src.fonts.font_manager import FontKey
from src.graphics.meshes.line import Line
from src.graphics.super_meshes import AlignEnum, FontSequence

from ..graphics.super_meshes.button import (
    Button,
    ButtonState,
    ButtonTextConfig,
)

if TYPE_CHECKING:
    from src.game.game import Game

from src.core.displayable import Displayable
from src.graphics import Color, Mesh, OperationEnum, Position
from src.graphics.mesh_layer import LayerProtocol, MeshLayer
from src.graphics.meshes import Plane

from .generators.popup_generator import generate_popup_bg
from .interface import Interface


class CheatInterface(Interface):
    game: 'Game'
    hiden: bool
    layer: MeshLayer

    def __init__(self, game: 'Game') -> None:
        self.game = game
        self.hidden = True
        self.layer = MeshLayer()

        screen_width = self.game._screen.width
        screen_height = self.game._screen.height
        config = self.game._config
        size = self.game._app.size
        fonts = self.game._app.fonts

        self.layer.meshes.append(Plane(
            Color(*config.pause_menu_overlay_color, 150),
            (
                Position(0, 0), Position(screen_width, screen_height)
            ),
            OperationEnum.ALPHA,
            dynamic=True,
        ))

        width: int = 856
        height: int = 568
        width_middle: int = screen_width // 2

        popup_position, popup_size, popup_plane, popup_border = \
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
                popup_position.y + size.get(506.5 + 15)
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

        self.layer.meshes.append(Button(
            position=Position(
                popup_position.x + size.get(596),
                popup_position.y + size.get(492)
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

        lines_params: list[int] = [201, 471]
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

    def hide(self) -> None:
        self.hidden = True
        for mesh in self.get_layer().meshes:
            self._set_hidden(mesh, True)

    def display(self) -> None:
        self.hidden = False
        for mesh in self.get_layer().meshes:
            self._set_hidden(mesh, False)

    @staticmethod
    def _set_hidden(
                mesh: Mesh | LayerProtocol | MeshLayer | Displayable,
                hidden: bool
            ) -> None:
        if isinstance(mesh, MeshLayer):
            for child in mesh.meshes:
                CheatInterface._set_hidden(child, hidden)
            return
        if isinstance(mesh, Mesh | Displayable):
            mesh.set_hidden(hidden)
        if isinstance(mesh, LayerProtocol):
            CheatInterface._set_hidden(mesh.get_layer(), hidden)

    def action_open(self) -> None:
        self.display()

    def action_close(self) -> None:
        self.hide()

    def get_layer(self) -> MeshLayer:
        return self.layer
