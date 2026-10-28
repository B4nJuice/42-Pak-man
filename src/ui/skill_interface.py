from typing import TYPE_CHECKING

from src.fonts import FontKey
from src.game.ameliorations.skills.skill import Skill
from src.game.ameliorations.skills.skill_type import SkillType
from src.graphics import MeshLayer
from src.graphics.color import Color
from src.graphics.meshes.plane import Plane
from src.graphics.position import Position
from src.graphics.super_meshes import AlignEnum
from src.graphics.super_meshes.font_sequence import FontSequence
from src.ui.amelioration_interface import Rectangle
from src.ui.interface import Interface

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
                skill_value_fontkey: FontKey = FontKey.BOLD_24,
                skill_title_font_size: float = 23,
                skill_value_font_size: float = 55.5,
            ) -> None:
        super().__init__(game)
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
            thickness=2,
            smooth_end=True
        )

        size = self.game._app.size

        self.title = FontSequence(
            title,
            self.game._app.fonts.get(skill_title_fontkey),
            Color(*self.game._config.skill_interface_title_color),
            Position(
                position.x + size.get(8),
                position.y + size.get(skill_title_font_size)
            ),
            spacing=1,
            align=AlignEnum.LEFT
        )

        self.value = FontSequence(
            self._format_skill(type(self.skill)),
            self.game._app.fonts.get(skill_value_fontkey),
            Color(*self.game._config.skill_interface_value_color),
            Position(
                position.x + size.get(8),
                position.y + size.get(skill_value_font_size)
            ),
            spacing=1,
            align=AlignEnum.LEFT,
            dynamic=True
        )

        self.layer.meshes.append(self.background)
        self.layer.meshes.append(self.border)
        self.layer.meshes.append(self.title)
        self.layer.meshes.append(self.value)

    def refresh(self) -> None:
        self.value.set_sequence_text(self._format_skill(type(self.skill)))

    def get_layer(self) -> MeshLayer:
        return self.layer

    def _format_skill(self, skill_type: type[Skill]) -> str:
        player = self.game._player
        skill = skill_type()
        value = self.default_value + sum(
            amelioration.get_skill(skill_type).get_value()
            for amelioration in player._ameliorations.gets(skill_type)
        )
        if skill.get_type() == SkillType.STATIC:
            return f"{value:.2f}{skill.get_suffix()}"
        return f"{1 + value / 100:.2f}x"
