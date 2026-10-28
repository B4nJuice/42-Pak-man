from typing import TYPE_CHECKING

from src.graphics.meshes.plane import Plane

if TYPE_CHECKING:
    from src.game.game import Game

from src.fonts import FontKey
from src.game.ameliorations import (
    ExpSkill,
    LuckSkill,
    PowerSkill,
    SpeedSkill,
    SuperTimeSkill,
)
from src.graphics import Color, Position
from src.graphics.mesh_layer import MeshLayer
from src.graphics.super_meshes import AlignEnum, Bar, FontSequence, Rectangle

from .amelioration_placeholder_interface import (
    AmeliorationPlaceholderInterface,
)
from .interface import Interface
from .skill_interface import SkillInterface


class StatsInterface(Interface):
    def __init__(self, game: 'Game') -> None:
        super().__init__(game)
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
                Position(
                    self.game._app.size.get(27),
                    self.game._app.size.get(15)
                ),
                Position(
                    self.game._app.size.get(27 + 265),
                    self.game._app.size.get(15 + 689)
                )
            ),
        )

        self.border: Rectangle = Rectangle(
            Color(*self.game._config.stats_border_color),
            Position(self.game._app.size.get(27), self.game._app.size.get(15)),
            self.game._app.size.get(265),
            self.game._app.size.get(689),
            3,
            dynamic=True,
            smooth_end=True
        )

        title_font_size = self.game._app.size.get(43)
        self.title: FontSequence = FontSequence(
            "STATS",
            self.game._app.fonts.get(FontKey.TITLE_36),
            Color(*self.game._config.stats_text_color),
            Position(
                (self.x_offset + self.width) // 2,
                (
                    self.y_offset +
                    self.game._app.size.get(38) +
                    title_font_size // 2
                ),
            ),
            align=AlignEnum.CENTER,
        )

        content_left = self.x_offset + self.game._app.size.get(20)

        self.lives_text = FontSequence(
            "LIVES",
            self.game._app.fonts.get(FontKey.BOLD_10),
            Color(*self.game._config.lives_text_color),
            Position(
                content_left,
                self.y_offset + self.game._app.size.get(115.5)
            ),
            align=AlignEnum.LEFT,
        )

        self.lives_number = FontSequence(
            "3/3",
            self.game._app.fonts.get(FontKey.BOLD_10),
            Color(*self.game._config.lives_number_color),
            Position(
                content_left + self.game._app.size.get(225),
                self.y_offset + self.game._app.size.get(115.5)
            ),
            align=AlignEnum.RIGHT,
        )

        max_lives = self.game._player._max_lives
        lives_bar_width = self.game._app.size.get(225)
        lives_bar_gap = self.game._app.size.get(6)
        single_bar_width = max(
            1,
            (
                lives_bar_width
                - lives_bar_gap * max(0, max_lives - 1)
            ) // max_lives,
        )
        self.lives_bars = [
            Bar(
                Color(*self.game._config.lives_bar_fill_color),
                Color(*self.game._config.lives_bar_border_color),
                Position(
                    content_left
                    + index * (single_bar_width + lives_bar_gap),
                    self.y_offset + self.game._app.size.get(129),
                ),
                single_bar_width,
                self.game._app.size.get(8),
                border_thickness=1,
                goal=1,
                progression=0,
                dynamic=True,
                smooth_end=True,
            )
            for index in range(max_lives)
        ]

        skill_y = self.y_offset + self.game._app.size.get(155)

        skill_gap = self.game._app.size.get(12)
        skill_width = self.game._app.size.get(106.5)
        skill_height = self.game._app.size.get(53)
        skill_title_font_size = 13
        skill_value_font_size = 40
        skills = (
            ("SPEED", SpeedSkill),
            ("LUCK", LuckSkill),
            ("POWER", PowerSkill),
            ("EXP", ExpSkill),
        )
        self.skill_interfaces = [
            SkillInterface(
                self.game,
                skill_type(),
                title,
                Position(
                    content_left
                    + (index % 2) * (skill_width + skill_gap),
                    skill_y + (index // 2) * (skill_height + skill_gap),
                ),
                skill_width,
                skill_height,
                skill_title_fontkey=FontKey.BOLD_8,
                skill_value_fontkey=FontKey.BOLD_18,
                skill_title_font_size=skill_title_font_size,
                skill_value_font_size=skill_value_font_size
            )
            for index, (title, skill_type) in enumerate(skills)
        ]
        self.skill_interfaces.append(
            SkillInterface(
                self.game,
                SuperTimeSkill(),
                "SUPER TIME",
                Position(
                    content_left,
                    skill_y + 2 * (skill_height + skill_gap),
                ),
                self.game._app.size.get(225),
                self.game._app.size.get(72),
                self.game._level.state.frightened_phase.get_default(),
            )
        )

        self.amelioration_text = FontSequence(
            "AMELIORATIONS",
            self.game._app.fonts.get(FontKey.BOLD_10),
            Color(*self.game._config.lives_text_color),
            Position(
                content_left,
                self.y_offset + self.game._app.size.get(386)
            ),
            align=AlignEnum.LEFT,
        )

        placeholder_y = self.y_offset + self.game._app.size.get(404)
        placeholder_size = self.game._app.size.get(64)
        placeholder_gap = (
            self.game._app.size.get(225) -
            placeholder_size * 3
        ) // 2
        placeholder_size = max(1, placeholder_size)
        self.amelioration_placeholders = [
            AmeliorationPlaceholderInterface(
                self.game,
                Position(
                    content_left
                    + index * (placeholder_size + placeholder_gap),
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
        self.layer.meshes.append(self.lives_text)
        self.layer.meshes.append(self.lives_number)
        for lives_bar in self.lives_bars:
            self.layer.meshes.append(lives_bar)
        for skill_interface in self.skill_interfaces:
            self.layer.meshes.append(skill_interface)

        self.layer.meshes.append(self.amelioration_text)

        for placeholder in self.amelioration_placeholders:
            self.layer.meshes.append(placeholder)

        self.refresh()
        self.refresh_ameliorations()

    def refresh(self) -> None:
        player = self.game._player

        for skill_interface in self.skill_interfaces:
            skill_interface.refresh()

        self.lives_number.set_sequence_text(
            f"{player._lives}/{player._max_lives}"
        )
        for index, lives_bar in enumerate(self.lives_bars):
            lives_bar.set_progression(
                1 if index < player._lives else 0
            )

    def refresh_ameliorations(self) -> None:
        ameliorations = self.game._player._ameliorations.all()
        for placeholder, amelioration in zip(
                self.amelioration_placeholders, ameliorations
        ):
            placeholder.set_amelioration(amelioration)

    def get_layer(self) -> MeshLayer:
        return self.layer
