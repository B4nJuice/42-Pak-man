from typing import TYPE_CHECKING

from src.fonts.font_manager import FontKey
from src.graphics.super_meshes import FontSequence

if TYPE_CHECKING:
    from src.game.game import Game

from src.core.displayable import Displayable
from src.game.game_status import GameStatus
from src.graphics import Color, Mesh, OperationEnum, Position
from src.graphics.mesh_layer import LayerProtocol, MeshLayer
from src.graphics.meshes import Plane

from .generators.popup_generator import generate_popup_bg
from .interface import Interface


class EscapeInterface(Interface):
    def __init__(self, game: 'Game') -> None:
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
            dynamic=True,
        )

        width: int = 520
        height: int = 465
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

        for text in texts:
            self.layer.meshes.append(text)

        # buttons_params: list[dict[str, Any]] = [
        #     {
        #         'label': 'RESUME',
        #         'lavel_hover': '> RESUME',
        #         'action_key_label': 'ESC',
        #         'action_key': None,
        #         'action': None
        #     },
        #     {
        #         'label': 'SETTINGS',
        #         'lavel_hover': '> SETTINGS',
        #         'action_key_label': None,
        #         'action_key': None,
        #         'action': None
        #     },
        #     {
        #         'label': 'MAIN MENU',
        #         'lavel_hover': '> MAIN MENU',
        #         'action_key_label': None,
        #         'action_key': None,
        #         'action': self.end
        #     }
        # ]

#         self.buttons: list[tuple[Plane, Rectangle, FontSequence]] = []
#         for index, params in enumerate(buttons_params):
#             label: str = params['label']
#             on_click: Any = params['action']
#
#             y = first_button_y + index * (button_height + button_gap)
#             button = Plane(
#                 Color(*config.menu_button_color),
#                 (
#                     Position(button_x, y),
#                     Position(button_x + button_width, y + button_height)
#                 ),
#                 OperationEnum.ALPHA,
#                 dynamic=True,
#                 on_click=on_click
#             )
#             border = Rectangle(
#                 Color(*config.menu_border_color),
#                 Position(button_x, y),
#                 button_width,
#                 button_height,
#                 2,
#                 dynamic=True,
#                 smooth_end=True,
#             )
#             text = FontSequence(
#                 label,
#                 self.game._font,
#                 Color(*config.menu_text_color),
#                 Position(
#                     button_x + button_width // 2,
#                     y + button_height // 2 + 8
#                 ),
#                 spacing=4,
#                 align=AlignEnum.CENTER,
#                 dynamic=True,
#             )
#             self.buttons.append((button, border, text))

        self.hide()

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
                EscapeInterface._set_hidden(child, hidden)
            return
        if isinstance(mesh, Mesh | Displayable):
            mesh.set_hidden(hidden)
        if isinstance(mesh, LayerProtocol):
            EscapeInterface._set_hidden(mesh.get_layer(), hidden)

    def start(self) -> None:
        self.display()
        self.game.set_status(GameStatus.PAUSED)

    def end(self) -> None:
        self.hide()
        self.game.set_status(GameStatus.RUNNING)

    def get_layer(self) -> MeshLayer:
        return self.layer
