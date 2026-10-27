from collections.abc import Callable
from copy import deepcopy
from typing import TYPE_CHECKING

from src.core.displayable import SimpleDisplayable
from src.fonts.font_manager import FontKey
from src.game.ameliorations.amelioration import Amelioration
from src.game.ameliorations.skills.skill import Skill
from src.graphics.color import Color, OperationEnum
from src.graphics.mesh_layer import MeshLayer
from src.graphics.meshes.plane import Plane
from src.graphics.position import Position
from src.graphics.super_meshes import AlignEnum, FontSequence, Rectangle
from src.ui.interface import Interface
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
    rarity_color: Color

    def __init__(
                self,
                game: 'Game',
                position: Position,
                on_choose: Callable[[], None] | None = None,
                on_hover: Callable[[], None] | None = None,
            ) -> None:
        super().__init__(game)
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
            ),
            on_click=on_choose,
            on_hover=on_hover,
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
                self.position.x + self.size.get(21),
                self.position.y + self.size.get(15 + 10),
            ),
            align=AlignEnum.LEFT,
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

        self.skill_upgrade = FontSequence(
            "",
            self.game._app.fonts.get(FontKey.TEXT_6),
            Color(*self.game._config.skill_upgrade_color),
            Position(
                self.position.x + self.size.get(21),
                self.position.y + self.size.get(224),
            ),
            align=AlignEnum.LEFT,
            dynamic=True,
        )

        self.skill_change = FontSequence(
            "",
            self.game._app.fonts.get(FontKey.BOLD_8),
            Color(*self.game._config.skill_change_color),
            Position(
                self.position.x + self.size.get(172),
                self.position.y + self.size.get(213),
            ),
            align=AlignEnum.RIGHT,
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
        self.layer.meshes.append(self.skill_upgrade)
        self.layer.meshes.append(self.skill_change)

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

        _rarity_color: Color = Color(
            rarity_color[0],
            rarity_color[1],
            rarity_color[2],
            23,
        )
        self.amelioration_rarity_background.set_color(_rarity_color)
        self.amelioration_rarity_background.set_width(
            self.amelioration_rarity_text.total_width + self.size.get(12)
        )

        self.rarity_color = deepcopy(_rarity_color)
        self.rarity_color.set_alpha(255)

        skill_names = []
        skill_upgrades = []
        skill_changes = []
        skill_change_highlight_indexes: list[int] = []
        skill_change_index = 0
        for skill, skill_value in upgrades:
            before = float(skill.get_value())
            after = before + skill_value
            suffix = skill.get_suffix()
            before_text = f"{before:.2f}{suffix}"
            after_text = f"{after:.2f}{suffix}"
            change_text = f"{before_text} → {after_text}"

            skill_names.append(skill.get_name())
            skill_upgrades.append(
                f"+{skill_value:.2f} {suffix} {skill.get_name()}"
            )
            skill_changes.append(change_text)
            arrow_index = skill_change_index + len(before_text) + 1
            after_start = arrow_index + len("→ ")
            skill_change_highlight_indexes.extend(
                range(arrow_index, after_start + len(after_text))
            )
            skill_change_index += len(change_text) + len(" / ")

        self.skill_name.set_sequence_text(" / ".join(skill_names))
        self.skill_upgrade.set_sequence_text(" / ".join(skill_upgrades))
        self.skill_change.set_sequence_text(" / ".join(skill_changes))
        self.skill_change.set_color_indexes(
            self.rarity_color,
            skill_change_highlight_indexes
        )

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

    def select(self) -> None:
        self.border.set_thickness(2)
        self.border.set_color(self.rarity_color)
        self.choose_button_background.set_color(self.rarity_color)
        self.choose_button_text.set_sequence_text("> CHOOSE UPGRADE <")
        self.choose_button_text.set_color(
            Color(*self.game._config.selected_choose_button_color)
        )

    def unselect(self) -> None:
        self.border.set_thickness(1)
        self.border.set_color(
            Color(*self.game._config.amelioration_card_border_color)
        )
        self.choose_button_background.set_color(
            Color(*self.game._config.choose_button_background_color)
        )
        self.choose_button_text.set_sequence_text("CHOOSE UPGRADE")
        self.choose_button_text.set_color(
            Color(*self.game._config.choose_button_text_color)
        )

    def get_layer(self) -> MeshLayer:
        return self.layer
