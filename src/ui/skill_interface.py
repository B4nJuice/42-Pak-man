from typing import TYPE_CHECKING

from src.game.ameliorations.skills.skill import Skill
from src.game.ameliorations.skills.skill_type import SkillType
from src.graphics import MeshLayer
from src.graphics.color import Color
from src.graphics.meshes.plane import Plane
from src.graphics.position import Position
from src.graphics.super_meshes.font_sequence import FontSequence
from src.ui.amelioration_interface import Rectangle
from src.ui.interface import Interface
from src.utils.font_manager import FontKey

if TYPE_CHECKING:
    from src.game import Game


class SkillInterface(Interface):
    layer: MeshLayer
    skill: Skill
    position: Position
    width: int
    height: int
    game: 'Game'
    background: Plane
    title: FontSequence
    default_value: float

    def __init__(
                self,
                game: 'Game',
                skill: Skill,
                title: str,
                position: Position,
                width: int,
                height: int,
                default_value: float = 0,
                skill_title_fontkey: FontKey = FontKey.BOLD_10,
                skill_value_fontkey: FontKey = FontKey.BOLD_24
            ) -> None:
        self.game = game
        self.layer = MeshLayer()

        self.skill = skill
        self.width = width
        self.height = height
        self.default_value = default_value

        self.background = Plane(
            Color(*self.game._config.skill_interface_background_color),
            (
                position,
                Position(position.x + width, position.y + height)
            )
        )

        self.border = Rectangle(
            Color(*self.game._config.skill_interface_border_color),
            position,
            width,
            height,
            2
        )

        self.title = FontSequence(
            title,
            self.game._app.fonts.get(skill_title_fontkey),
            Color(*self.game._config.skill_interface_title_color),
            Position(position.x + width // 20, position.y + height // 3),
            spacing=1
        )

        self.value = FontSequence(
            self._format_skill(type(self.skill)),
            self.game._app.fonts.get(skill_value_fontkey),
            Color(*self.game._config.skill_interface_value_color),
            Position(position.x + width // 20, position.y + height // 3 * 2),
            spacing=1
        )

        self.layer.meshes.append(self.background)
        self.layer.meshes.append(self.border)
        self.layer.meshes.append(self.title)

    def _format_skill(self, skill_type: type[Skill]) -> str:
        player = self.game._player
        skill = skill_type()
        value =self.default_value + sum(
            amelioration.get_skill(skill_type).get_value()
            for amelioration in player._ameliorations.gets(skill_type)
        )
        if skill.get_type() == SkillType.STATIC:
            return f"{value:.1f}{skill._suffix}"
        return f" x{1 + value / 100:.1f}"
