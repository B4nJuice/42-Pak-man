from typing import TYPE_CHECKING

from src.graphics.meshes.plane import Plane

if TYPE_CHECKING:
    from src.game.game import Game
from src.game.ameliorations import (
    ExpSkill,
    LuckSkill,
    PowerSkill,
    SpeedSkill,
)
from src.game.ameliorations.skills.skill import Skill
from src.game.ameliorations.skills.skill_type import SkillType
from src.graphics import Color, Position
from src.graphics.font import Font
from src.graphics.mesh_layer import MeshLayer
from src.graphics.super_meshes import AlignEnum, FontSequence, Rectangle
from src.texture.font_keys import FontKeys

from .amelioration_placeholder_interface import (
    AmeliorationPlaceholderInterface,
)
from .interface import Interface


class StatsInterface(Interface):
    def __init__(self, game: 'Game') -> None:
        self.game: Game = game
        self.layer: MeshLayer = MeshLayer()

        self.x_offset: int = round(self.game._config.screen_width * 0.02)
        self.y_offset: int = round(self.game._config.screen_height * 0.02)
        self.width: int = round(self.game._config.screen_width * 0.25)\
            - self.x_offset
        self.height: int = self.game._config.screen_height - self.y_offset

        self.background: Plane = Plane(
            Color(*self.game._config.stats_background_color),
            (
                Position(self.x_offset, self.y_offset),
                Position(self.width, self.height)
            ),
        )

        self.border: Rectangle = Rectangle(
            Color(*self.game._config.stats_border_color),
            Position(self.x_offset, self.y_offset),
            self.width - self.x_offset,
            self.height - self.y_offset,
            3,
            dynamic=True,
            smooth_end=True
        )

        title_font_size = self.game._config.screen_height // 22
        self.title: FontSequence = FontSequence(
            "Stats",
            self.game._font,
            Color(*self.game._config.stats_text_color),
            Position(
                self.x_offset + self.width // 2,
                self.y_offset + title_font_size + 12,
            ),
            spacing=1,
            align=AlignEnum.CENTER,
            dynamic=True,
        )
        stats_font_size = max(10, self.game._config.screen_height // 42)
        self._stats_font = Font(
            self.game._app.texture.get_font(FontKeys.DEFAULT).as_posix(),
            self.game._screen.moderngl_context,
            pixel_size=stats_font_size,
        )
        self.stats: list[FontSequence] = [
            FontSequence(
                "",
                self._stats_font,
                Color(*self.game._config.stats_text_color),
                Position(
                    self.x_offset + 12,
                    self.y_offset + title_font_size + 42
                    + index * (stats_font_size + 5),
                ),
                spacing=1,
                align=AlignEnum.LEFT,
                dynamic=True,
            )
            for index in range(7)
        ]
        placeholder_y = (
            self.y_offset + title_font_size + 42
            + 7 * (stats_font_size + 5) + 18
        )
        content_left = self.x_offset + 12
        content_right = self.width - 12
        content_bottom = self.height - 12
        placeholder_gap = 6
        placeholder_size = min(
            (content_right - content_left - 2 * placeholder_gap) // 3,
            content_bottom - placeholder_y,
        )
        placeholder_size = max(1, placeholder_size)
        self.amelioration_placeholders = [
            AmeliorationPlaceholderInterface(
                self.game,
                Position(
                    content_left
                    + index * (placeholder_size + 6),
                    placeholder_y,
                ),
                placeholder_size,
                placeholder_size,
            )
            for index in range(3)
        ]

        self.layer.meshes.append(self.background)
        self.layer.meshes.append(self.border)
        self.layer.meshes.append(self.title)
        for stat in self.stats:
            self.layer.meshes.append(stat)
        for placeholder in self.amelioration_placeholders:
            self.layer.meshes.append(placeholder)
        self.refresh()
        self.refresh_ameliorations()

    def refresh(self) -> None:
        player = self.game._player
        values = (
            f"Level: {player._actual_level}",
            f"Experience: {player._exp_points:.1f}",
            f"Speed: {self._format_skill(SpeedSkill)}",
            f"Luck: {self._format_skill(LuckSkill)}",
            f"Power: {self._format_skill(PowerSkill)}",
            f"Exp: {self._format_skill(ExpSkill)}",
            f"Super time: {self._format_super_time()}",
        )
        for stat, value in zip(self.stats, values):
            stat.set_sequence_text(value)

    def refresh_ameliorations(self) -> None:
        ameliorations = self.game._player._ameliorations.all()
        for placeholder, amelioration in zip(
                self.amelioration_placeholders, ameliorations
        ):
            placeholder.set_amelioration(amelioration)

    def _format_skill(self, skill_type: type[Skill]) -> str:
        player = self.game._player
        skill = skill_type()
        value = sum(
            amelioration.get_skill(skill_type).get_value()
            for amelioration in player._ameliorations.gets(skill_type)
        )
        if skill.get_type() == SkillType.STATIC:
            return f"{value:.1f}{skill._suffix}"
        return f" x{1 + value / 100:.2f}"

    def _format_super_time(self) -> str:
        default_time = self.game._level.state.frightened_phase.get_default()
        additional_time = self.game._player.get_additional_super_time()
        return f"{default_time + additional_time:.1f}s"

    def get_layer(self) -> MeshLayer:
        return self.layer
