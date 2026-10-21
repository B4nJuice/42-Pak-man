from typing import TYPE_CHECKING, Any

from src.texture.font_keys import FontKeys

if TYPE_CHECKING:
    from src.game.game import Game

from src.core.displayable import Displayable, SimpleDisplayable
from src.game.ameliorations import Amelioration, AmeliorationRarity, Skill
from src.game.ameliorations.skills.skill_type import SkillType
from src.game.game_status import GameStatus
from src.graphics import Color, Mesh, OperationEnum, Position
from src.graphics.font import Font
from src.graphics.mesh_layer import MeshLayer
from src.graphics.meshes import Plane
from src.graphics.super_meshes import AlignEnum, FontSequence, Rectangle

from .interface import Interface


class AmeliorationInterface(Interface):
    _next_ameliorations: list[
        tuple[Amelioration, AmeliorationRarity, list[tuple[Skill, float]]]
    ]

    def __init__(self, game: 'Game') -> None:
        self.game: Game = game
        self.hidden: bool = True
        self.layer: MeshLayer = MeshLayer()
        self._next_ameliorations = []

        screen_width = self.game._screen.width
        screen_height = self.game._screen.height
        config = self.game._config
        context = self.game._screen.moderngl_context
        self._title_font = Font(
            game._app.texture.get_font(FontKeys.DEFAULT).as_posix(),
            context,
            config.amelioration_title_font_size
        )
        self._rarity_font = Font(
            game._app.texture.get_font(FontKeys.DEFAULT).as_posix(),
            context,
            config.amelioration_rarity_font_size
        )
        self._skill_font = Font(
            game._app.texture.get_font(FontKeys.DEFAULT).as_posix(),
            context,
            config.amelioration_skill_font_size
        )
        self._skill_line_count = max(
            1,
            max(
                len(amelioration().get_skills())
                for amelioration in Amelioration.__subclasses__()
            )
        )

        self.background = Plane(
            Color(*config.menu_overlay_color, 150),
            (
                Position(0, 0), Position(screen_width, screen_height)
            ),
            OperationEnum.ALPHA,
            dynamic=True,
        )

        panel_width = min(
            max(round(screen_width * 0.72), 520), screen_width - 32
        )
        button_width = round(panel_width * 0.88)
        line_gap = 4
        content_height = (
            config.amelioration_title_font_size
            + config.amelioration_rarity_font_size
            + self._skill_line_count * config.amelioration_skill_font_size
            + 3 * line_gap
        )
        button_height = max(
            round(screen_height * 0.18), content_height + 24
        )
        button_gap = max(round(screen_height * 0.025), 12)
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
                "label": "Amelioration",
                "on_click": lambda: self._choose_amelioration(0)
            },
            {
                "label": "Amelioration",
                "on_click": lambda: self._choose_amelioration(1)
            },
            {
                "label": "Amelioration",
                "on_click": lambda: self._choose_amelioration(2)
            },
        ]

        self.buttons: list[
            tuple[Plane, Rectangle, SimpleDisplayable, list[FontSequence]]
        ] = []
        icon_offset = 12
        icon_size = button_height - 2 * icon_offset
        text_left = button_x + icon_offset + icon_size + icon_offset
        text_right = button_x + button_width - icon_offset
        text_center = (text_left + text_right) // 2
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
            icon = SimpleDisplayable(
                self.game._app,
                'amelioration-exp',
                icon_size,
                icon_size,
                Position(
                    button_x + icon_offset + icon_size // 2,
                    y + button_height // 2,
                ),
            )
            title = FontSequence(
                label,
                self._title_font,
                Color(*config.menu_text_color),
                Position(
                    text_center,
                    y + 12 + config.amelioration_title_font_size
                ),
                spacing=4,
                align=AlignEnum.CENTER,
                dynamic=True,
            )
            rarity = FontSequence(
                "",
                self._rarity_font,
                Color(*config.menu_text_color),
                Position(
                    text_center,
                    y + 12 + config.amelioration_title_font_size
                    + line_gap + config.amelioration_rarity_font_size
                ),
                spacing=2,
                align=AlignEnum.CENTER,
                dynamic=True,
            )
            skill_lines = [
                FontSequence(
                    "",
                    self._skill_font,
                    Color(*config.menu_text_color),
                    Position(
                        text_center,
                        y + 12 + config.amelioration_title_font_size
                        + config.amelioration_rarity_font_size
                        + 2 * line_gap
                        + config.amelioration_skill_font_size
                        + skill_index * (
                            config.amelioration_skill_font_size + line_gap
                        )
                    ),
                    spacing=2,
                    align=AlignEnum.CENTER,
                    dynamic=True,
                )
                for skill_index in range(self._skill_line_count)
            ]
            texts = [title, rarity, *skill_lines]
            self.buttons.append((button, border, icon, texts))

        self.layer.meshes.append(self.background)
        self.layer.meshes.append(self.panel)
        self.layer.meshes.append(self.panel_border)
        for button, border, icon, texts in self.buttons:
            self.layer.meshes.append(button)
            self.layer.meshes.append(border)
            self.layer.meshes.append(icon)
            for text in texts:
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
                mesh: Mesh | MeshLayer | Displayable,
                hidden: bool
            ) -> None:
        if isinstance(mesh, MeshLayer):
            for child in mesh.meshes:
                AmeliorationInterface._set_hidden(child, hidden)
            return
        mesh.set_hidden(hidden)
        if hasattr(mesh, "get_layer"):
            AmeliorationInterface._set_hidden(mesh.get_layer(), hidden)

    def start(self) -> None:
        self._next_ameliorations = []
        rarity_colors = self._rarity_colors()
        for index, amelioration in enumerate(
                self.game._player.get_next_ameliorations()
        ):
            rarity, upgrades = amelioration.next_upgrade(
                luck=self.game._player.get_luck(),
                power=self.game._player.get_upgrade_power(),
            )
            self._next_ameliorations.append(
                (amelioration, rarity, upgrades)
            )
            button, border, icon, texts = self.buttons[index]
            color = Color(*rarity_colors[rarity])
            button.set_color(color)
            border.set_color(color)
            icon.set_texture_key(amelioration.get_texture_key())
            texts[0].set_sequence_text(
                amelioration.get_name()
            )
            texts[1].set_sequence_text(rarity.name)
            for skill_index, text in enumerate(texts[2:]):
                text.set_sequence_text(
                    self._format_skill(upgrades, skill_index)
                )
        self.display()
        self.game.set_status(GameStatus.AMELIORATION)

    def _choose_amelioration(self, index: int) -> None:
        amelioration, _, upgrades = self._next_ameliorations[index]
        self.game._player.add_amelioration(amelioration)
        amelioration.level_up(upgrades)
        self.end()

    def _rarity_colors(self) -> dict[
            AmeliorationRarity, tuple[int, int, int]
    ]:
        config = self.game._config
        return {
            AmeliorationRarity.COMMON: config.amelioration_common_color,
            AmeliorationRarity.UNCOMMON: config.amelioration_uncommon_color,
            AmeliorationRarity.RARE: config.amelioration_rare_color,
            AmeliorationRarity.EPIC: config.amelioration_epic_color,
            AmeliorationRarity.LEGENDARY: config.amelioration_legendary_color,
            AmeliorationRarity.MYTHIC: config.amelioration_mythic_color,
        }

    @staticmethod
    def _format_skill(
            upgrades: list[tuple[Skill, float]], index: int
    ) -> str:
        if index >= len(upgrades):
            return ""
        skill, value = upgrades[index]
        skill_name = skill.__class__.__name__.removesuffix("Skill")
        suffix = "%" if skill.get_type() == SkillType.PERCENTAGE else ""
        return f"{skill_name} +{value:g}{suffix}"

    def end(self) -> None:
        self.hide()
        self.game.set_status(GameStatus.RUNNING)

    def get_layer(self) -> MeshLayer:
        return self.layer
