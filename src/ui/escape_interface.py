from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.game.game import Game

from src.core.displayable import Displayable
from src.game.game_status import GameStatus
from src.graphics import Color, Mesh, OperationEnum, Position
from src.graphics.mesh_layer import LayerProtocol, MeshLayer
from src.graphics.meshes import Plane
from src.graphics.super_meshes import AlignEnum, FontSequence, Rectangle

from .interface import Interface


class EscapeInterface(Interface):
    def __init__(self, game: 'Game') -> None:
        self.game: Game = game
        self.hidden: bool = True
        self.layer: MeshLayer = MeshLayer()

        screen_width = self.game._screen.width
        screen_height = self.game._screen.height
        config = self.game._config

        self.background = Plane(
            Color(*config.menu_overlay_color, 150),
            (
                Position(0, 0), Position(screen_width, screen_height)
            ),
            OperationEnum.ALPHA,
            dynamic=True,
        )

        panel_width = min(
            max(round(screen_width * 0.4), 280), screen_width - 48
        )
        button_width = round(panel_width * 0.68)
        button_height = max(round(screen_height * 0.08), 42)
        button_gap = max(round(screen_height * 0.035), 14)
        buttons_height = 3 * button_height + 2 * button_gap
        panel_padding = max(round(screen_height * 0.08), 32)
        panel_height = min(
            buttons_height + 2 * panel_padding, screen_height - 48
        )
        panel_x = (screen_width - panel_width) // 2
        panel_y = (screen_height - panel_height) // 2
        button_x = panel_x + (panel_width - button_width) // 2
        first_button_y = panel_y + (panel_height - buttons_height) // 2

        self.panel = Plane(
            Color(*config.menu_panel_color, 245),
            (
                Position(panel_x, panel_y),
                Position(panel_x + panel_width, panel_y + panel_height)
            ),
            OperationEnum.ALPHA,
            dynamic=True,
        )
        self.panel_border = Rectangle(
            Color(*config.menu_border_color),
            Position(panel_x, panel_y),
            panel_width,
            panel_height,
            3,
            dynamic=True,
            smooth_end=True,
        )

        button_params: list[dict[str, Any]] = [
            {
                "label": "Main Menu",
                "on_click": None
            },
            {
                "label": "Settings",
                "on_click": None
            },
            {
                "label": "Continue",
                "on_click": self.end
            },
        ]

        self.buttons: list[tuple[Plane, Rectangle, FontSequence]] = []
        for index, params in enumerate(button_params):
            label: str = params["label"]
            on_click: Any = params["on_click"]
            y = first_button_y + index * (button_height + button_gap)
            button = Plane(
                Color(*config.menu_button_color),
                (
                    Position(button_x, y),
                    Position(button_x + button_width, y + button_height)
                ),
                OperationEnum.ALPHA,
                dynamic=True,
                on_click=on_click
            )
            border = Rectangle(
                Color(*config.menu_border_color),
                Position(button_x, y),
                button_width,
                button_height,
                2,
                dynamic=True,
                smooth_end=True,
            )
            text = FontSequence(
                label,
                self.game._font,
                Color(*config.menu_text_color),
                Position(
                    button_x + button_width // 2,
                    y + button_height // 2 + 8
                ),
                spacing=4,
                align=AlignEnum.CENTER,
                dynamic=True,
            )
            self.buttons.append((button, border, text))

        self.layer.meshes.append(self.background)
        self.layer.meshes.append(self.panel)
        self.layer.meshes.append(self.panel_border)
        for button, border, text in self.buttons:
            self.layer.meshes.append(button)
            self.layer.meshes.append(border)
            self.layer.meshes.append(text)
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
