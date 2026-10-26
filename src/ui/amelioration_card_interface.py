from typing import TYPE_CHECKING

from src.core.displayable import SimpleDisplayable
from src.game.ameliorations.amelioration import Amelioration
from src.game.ameliorations.skills.skill import Skill
from src.graphics.color import Color, OperationEnum
from src.graphics.mesh_layer import MeshLayer
from src.graphics.meshes.plane import Plane
from src.graphics.position import Position
from src.graphics.super_meshes import AlignEnum, FontSequence, Rectangle
from src.ui.interface import Interface
from src.utils.font_manager import FontKey
from src.utils.size import SizeCore

if TYPE_CHECKING:
    from src.game.game import Game


class AmeliorationCardInterface(Interface):
    layer: MeshLayer
    position: Position
    width: int
    height: int
    amelioration: Amelioration | None
    background: Plane
    border: Rectangle
    icon: SimpleDisplayable | None
    level: FontSequence
    game: 'Game'
    size: SizeCore

    def __init__(
                self,
                game: 'Game',
                position: Position,
            ) -> None:
        self.layer = MeshLayer()
        self.position = position
        self.amelioration = None
        self.icon = None
        self.game = game
        self.size = self.game._app.size

        self.background = Plane(
            Color(*self.game._config.amelioration_card_color),
            (
                position,
                Position(
                    position.x + self.size.get(193),
                    position.y + self.size.get(289)
                )
            ),
            dynamic=False,
        )

        self.border = Rectangle(
            Color(*self.game._config.amelioration_card_border_color),
            position,
            self.size.get(193),
            self.size.get(289),
            thickness=1,
            smooth_end=True
        )

        self.amelioration_effect_background = Plane(
            Color(*self.game._config.amelioration_effect_background_color),
            (
                Position(
                    self.position.x + self.size.get(14),
                    self.position.y + self.size.get(200)
                ),
                Position(
                    self.position.x + self.size.get(163 + 14),
                    self.position.y + self.size.get(29 + 200)
                ),
            )
        )

        self.choose_button_background = Plane(
            Color(*self.game._config.choose_button_background_color),
            (
                Position(
                    self.position.x + self.size.get(14),
                    self.position.y + self.size.get(241)
                ),
                Position(
                    self.position.x + self.size.get(163 + 14),
                    self.position.y + self.size.get(29 + 241)
                ),
            )
        )

        self.choose_button_text = FontSequence(
            "CHOOSE UPGRADE",
            self.game._app.fonts.get(FontKey.BOLD_10),
            Color(*self.game._config.choose_button_text_color),
            Position(
                self.position.x + self.size.get(96.5),
                self.position.y + self.size.get(259),
            ),
            align=AlignEnum.CENTER,
            dynamic=True,
        )

        self.amelioration_rarity_background = Plane(
            Color(0, 0, 0, 0),
            (
                Position(
                    self.position.x + self.size.get(15),
                    self.position.y + self.size.get(15),
                ),
                Position(
                    self.position.x + self.size.get(15 + 61),
                    self.position.y + self.size.get(15 + 16),
                ),
            ),
            operation=OperationEnum.ALPHA,
            dynamic=True
        )

        self.level_text = FontSequence(
            "",
            self.game._app.fonts.get(FontKey.BOLD_8),
            Color(*self.game._config.amelioration_rarity_text_color),
            Position(
                self.position.x + self.size.get(178),
                self.position.y + self.size.get(18 + 10),
            ),
            align=AlignEnum.RIGHT,
            dynamic=True,
        )

        self.amelioration_rarity_text = FontSequence(
            "",
            self.game._app.fonts.get(FontKey.BOLD_8),
            Color(*self.game._config.amelioration_rarity_text_color),
            Position(
                self.position.x + self.size.get(15 + 30.5),
                self.position.y + self.size.get(15 + 10),
            ),
            align=AlignEnum.CENTER,
            dynamic=True,
        )

        self.amelioration_name = FontSequence(
            "",
            self.game._app.fonts.get(FontKey.TITLE_14),
            Color(*self.game._config.amelioration_name),
            Position(
                self.position.x + self.size.get(14),
                self.position.y + self.size.get(158),
            ),
            align=AlignEnum.LEFT,
            dynamic=True,
        )

        self.amelioration_description = FontSequence(
            "",
            self.game._app.fonts.get(FontKey.TEXT_8),
            Color(*self.game._config.amelioration_description),
            Position(
                self.position.x + self.size.get(14),
                self.position.y + self.size.get(181),
            ),
            align=AlignEnum.LEFT,
            dynamic=True,
        )

        self.skill_name = FontSequence(
            "",
            self.game._app.fonts.get(FontKey.TEXT_8),
            Color(*self.game._config.skill_name_color),
            Position(
                self.position.x + self.size.get(21),
                self.position.y + self.size.get(212),
            ),
            align=AlignEnum.LEFT,
            dynamic=True,
        )

        self.layer.meshes.append(self.background)
        self.layer.meshes.append(self.border)
        self.layer.meshes.append(self.amelioration_rarity_background)
        self.layer.meshes.append(self.amelioration_rarity_text)
        self.layer.meshes.append(self.amelioration_effect_background)
        self.layer.meshes.append(self.choose_button_background)
        self.layer.meshes.append(self.choose_button_text)
        self.layer.meshes.append(self.level_text)
        self.layer.meshes.append(self.skill_name)


    def set_amelioration(
                self,
                amelioration: Amelioration,
                upgrades: list[tuple[Skill, float]],
                rarity: tuple[str, tuple[int, int, int]]
            ) -> None:
        self.amelioration = amelioration
        if self.icon is not None:
            self.layer.meshes.remove(self.icon)
        if self.amelioration_name in self.layer.meshes:
            self.layer.meshes.remove(self.amelioration_name)
        if self.amelioration_description in self.layer.meshes:
            self.layer.meshes.remove(self.amelioration_description)

        rarity_name, rarity_color = rarity

        self.amelioration_rarity_text.set_sequence_text("✦ " + rarity_name)
        self.amelioration_rarity_text.set_color(Color(*rarity_color))

        rarity_color = list(rarity_color) + [23]
        self.amelioration_rarity_background.set_color(
            Color(*rarity_color)
        )
        skill = amelioration.get_skills()[0]

        self.skill_name.set_sequence_text(skill.get_name())

        self.icon = SimpleDisplayable(
            self.game._app,
            self.amelioration.get_texture_key(),
            self.size.get(75),
            self.size.get(75),
            Position(
                self.position.x + self.size.get(95.5),
                self.position.y + self.size.get(94.5)
            ),

        )

        self.level_text.set_sequence_text(
            f"LV. {
                self.amelioration.get_level()
            } → {self.amelioration.get_level() + 1}"
        )

        self.amelioration_name.set_sequence_text(
            amelioration.get_name().upper()
        )
        self.amelioration_description.set_sequence_text(
            amelioration.get_description()
        )

        self.layer.meshes.append(self.amelioration_name)
        self.layer.meshes.append(self.amelioration_description)
        self.layer.meshes.append(self.icon)

    def get_layer(self) -> MeshLayer:
        return self.layer
