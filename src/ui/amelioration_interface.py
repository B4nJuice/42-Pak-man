from typing import TYPE_CHECKING, Any

import pygame

from src.texture.font_keys import FontKeys
from src.utils.font_manager import FontKey

if TYPE_CHECKING:
    from src.game.game import Game

from src.core.displayable import Displayable, SimpleDisplayable
from src.game.ameliorations import Amelioration, AmeliorationRarity, Skill
from src.game.ameliorations.skills.skill_type import SkillType
from src.game.game_status import GameStatus
from src.graphics import Color, Mesh, OperationEnum, Position
from src.graphics.font import Font
from src.graphics.mesh_layer import LayerProtocol, MeshLayer
from src.graphics.meshes import Plane
from src.graphics.super_meshes import AlignEnum, FontSequence, Rectangle

from .interface import Interface


class AmeliorationInterface(Interface):
    _selection_scale: float = 1.08
    _next_ameliorations: list[
        tuple[Amelioration, AmeliorationRarity, list[tuple[Skill, float]]]
    ]

    def __init__(self, game: 'Game') -> None:
        self.game: Game = game
        self.hidden: bool = True
        self._selected_index = 0
        self.layer: MeshLayer = MeshLayer()
        self._next_ameliorations = []

        size = self.game._app.size

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
            Color(*config.menu_overlay_color, 120),
            (
                Position(0, 0), Position(screen_width, screen_height)
            ),
            OperationEnum.ALPHA,
            dynamic=True,
        )

        self.panel = Plane(
            Color(*config.menu_panel_color),
            (
                Position(size.get(280), size.get(120)),
                Position(size.get(280 + 722), size.get(120 + 482))
            ),
            OperationEnum.SET,
            dynamic=True,
        )

        self.panel_border = Rectangle(
            Color(*config.menu_border_color),
            Position(size.get(280), size.get(120)),
            size.get(722),
            size.get(482),
            2,
            dynamic=True,
            smooth_end=True,
        )

        self.back_level_up_text = FontSequence(
            "LEVEL UP!",
            self.game._app.fonts.get(FontKey.TITLE_40),
            Color(*self.game._config.back_level_up_color),
            Position(size.get(640), size.get(187))
        )

        self.level_up_text = FontSequence(
            "LEVEL UP!",
            self.game._app.fonts.get(FontKey.TITLE_40),
            Color(*self.game._config.level_up_color),
            Position(size.get(640), size.get(182))
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
            tuple[
                Plane,
                Plane,
                SimpleDisplayable,
                list[FontSequence],
                FontSequence,
            ]
        ] = []
        icon_offset = 12
        icon_size = button_height - 2 * icon_offset
        self._icon_size = icon_size
        text_left = button_x + icon_offset + icon_size + icon_offset
        text_right = button_x + button_width - icon_offset
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
            selected_button = Plane(
                Color(*config.menu_button_color),
                (
                    Position(button_x - 8, y - 8),
                    Position(
                        button_x + button_width + 8,
                        y + button_height + 8,
                    )
                ),
                OperationEnum.ALPHA,
                dynamic=True,
                on_click=on_click
            )
            icon = SimpleDisplayable(
                self.game._app,
                'amelioration-unknown',
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
                    text_left,
                    y + 12 + config.amelioration_title_font_size
                ),
                spacing=4,
                align=AlignEnum.LEFT,
                dynamic=True,
            )
            rarity = FontSequence(
                "",
                self._rarity_font,
                Color(*config.menu_text_color),
                Position(
                    text_left,
                    y + 12 + config.amelioration_title_font_size
                    + line_gap + config.amelioration_rarity_font_size
                ),
                spacing=2,
                align=AlignEnum.LEFT,
                dynamic=True,
            )
            skill_lines = [
                FontSequence(
                    "",
                    self._skill_font,
                    Color(*config.menu_text_color),
                    Position(
                        text_left,
                        y + 12 + config.amelioration_title_font_size
                        + config.amelioration_rarity_font_size
                        + 2 * line_gap
                        + config.amelioration_skill_font_size
                        + skill_index * (
                            config.amelioration_skill_font_size + line_gap
                        )
                    ),
                    spacing=2,
                    align=AlignEnum.LEFT,
                    dynamic=True,
                )
                for skill_index in range(self._skill_line_count)
            ]
            level = FontSequence(
                "",
                self._rarity_font,
                Color(*config.menu_text_color),
                Position(
                    text_right,
                    y + 12 + config.amelioration_title_font_size
                ),
                spacing=2,
                align=AlignEnum.RIGHT,
                dynamic=True,
            )
            texts = [title, rarity, *skill_lines]
            self.buttons.append(
                (
                    button,
                    selected_button,
                    icon,
                    texts,
                    level,
                )
            )

        self.layer.meshes.append(self.background)
        self.layer.meshes.append(self.panel)
        self.layer.meshes.append(self.panel_border)
        self.layer.meshes.append(self.back_level_up_text)
        self.layer.meshes.append(self.level_up_text)

        for (
            button,
            selected_button,
            icon,
            texts,
            level,
        ) in (
            self.buttons
        ):
            pass
            # self.layer.meshes.append(selected_button)
            # self.layer.meshes.append(button)
            # self.layer.meshes.append(icon)
            # for text in texts:
                # self.layer.meshes.append(text)
            # self.layer.meshes.append(level)
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
                AmeliorationInterface._set_hidden(child, hidden)
            return
        if isinstance(mesh, Mesh | Displayable):
            mesh.set_hidden(hidden)
        if isinstance(mesh, LayerProtocol):
            AmeliorationInterface._set_hidden(mesh.get_layer(), hidden)

    def start(self) -> None:
        self._next_ameliorations = []
        self._selected_index = 0
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
            (
                button,
                selected_button,
                icon,
                texts,
                level,
            ) = (
                self.buttons[index]
            )
            color = Color(*rarity_colors[rarity])
            button.set_color(color)
            selected_button.set_color(color)
            icon.set_texture_key(amelioration.get_texture_key())
            texts[0].set_sequence_text(
                amelioration.get_name()
            )
            texts[1].set_sequence_text(rarity.name)
            level.set_sequence_text(
                f"Level {amelioration.get_level() + 1}"
            )
            for skill_index, text in enumerate(texts[2:]):
                text.set_sequence_text(
                    self._format_skill(upgrades, skill_index)
                )
        self.display()
        self._update_selection()
        self.game.set_status(GameStatus.AMELIORATION)

    def handle_key(self, key: int) -> bool:
        if self.hidden:
            return False
        if key in (pygame.K_UP, pygame.K_LEFT):
            self._selected_index = (self._selected_index - 1) % 3
            self._update_selection()
            return True
        if key in (pygame.K_DOWN, pygame.K_RIGHT):
            self._selected_index = (self._selected_index + 1) % 3
            self._update_selection()
            return True
        if key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            self._choose_amelioration(self._selected_index)
            return True
        return False

    def _update_selection(self) -> None:
        for index, button_data in enumerate(self.buttons):
            selected_button = button_data[1]
            selected_button.set_hidden(index != self._selected_index)
            button = button_data[0]
            icon = button_data[2]
            scale = (
                self._selection_scale
                if index == self._selected_index
                else 1.0
            )
            button.set_hidden(False)
            icon.set_width(round(self._icon_size * scale))
            icon.set_height(round(self._icon_size * scale))

    def _choose_amelioration(self, index: int) -> None:
        amelioration, _, upgrades = self._next_ameliorations[index]
        amelioration.level_up(upgrades)
        self.game._player.add_amelioration(amelioration)
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
        suffix = (
            "%" if skill.get_type() == SkillType.PERCENTAGE else skill._suffix
        )
        before = float(skill.get_value())
        after = float(before + value)
        return f"{skill_name} {before:.2f}{suffix} -> {after:.2f}{suffix}"

    def end(self) -> None:
        self.hide()
        self.game.set_status(GameStatus.RUNNING)

    def get_layer(self) -> MeshLayer:
        return self.layer
