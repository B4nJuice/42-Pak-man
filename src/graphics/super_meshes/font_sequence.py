from enum import Enum

from src.graphics import Color, OperationEnum, Position
from src.graphics.font import Font
from src.graphics.meshes import Character
from src.graphics.super_mesh import MeshLayer, SuperMesh


class AlignEnum(Enum):
    LEFT = "LEFT"
    CENTER = "CENTER"
    RIGHT = "RIGHT"


class FontSequence(SuperMesh):
    font: Font
    position: Position
    spacing: int
    layer: MeshLayer
    characters: list[Character]
    align: AlignEnum
    text: str
    scale: float
    total_width: int

    def __init__(
                self,
                text: str,
                font: Font,
                color: Color,
                position: Position,
                spacing: int = 0,
                align: AlignEnum = AlignEnum.CENTER,
                operation: OperationEnum = OperationEnum.ALPHA,
            ) -> None:
        """
        Initialize the instance.

        Args:
            text: Text used by the operation.
            font: Font used by the operation.
            color: Color applied to the rendered element.
            position: Screen or world coordinates of the object.
            spacing: Spacing used by the operation.
            align: Align used by the operation.
            operation: Operation used by the operation.
        """
        super().__init__(
                color,
                operation,
            )

        self.font = font
        self.position = position
        self.spacing = spacing
        self.layer = MeshLayer()
        self.characters = []
        self.align = align if isinstance(align, AlignEnum) else\
            AlignEnum.CENTER
        self.scale = 1.0
        self.init()
        self.set_sequence_text(text)

    def init(self) -> None:
        """
        Initialize the associated state.
        """
        pass

    def set_color(self, color: Color) -> None:
        """
        Assign the color.

        Args:
            color: Color applied to the rendered element.
        """
        super().set_color(color)
        for char in self.characters:
            char.set_color(color)

    def set_color_indexes(
                self,
                color: Color,
                indexes: list[int] | None
            ) -> None:
        """
        Assign the color indexes.

        Args:
            color: Color applied to the rendered element.
            indexes: Indexes used by the operation.
        """
        if indexes is None:
            for char in self.characters:
                char.set_color(color)
        else:
            text_len = len(self.text)
            for i in indexes:
                if i >= text_len:
                    break
                self.characters[i].set_color(color)

    def set_sequence_text(self, text: str) -> None:
        """
        Assign the sequence text.

        Args:
            text: Text used by the operation.
        """
        self.text = text
        self.characters = []
        self.layer.meshes.clear()

        total_width = 0
        for index, character in enumerate(self.text):
            infos = self.font.get_characters()[character]
            total_width += infos["advance"]
            if index < len(self.text) - 1:
                total_width += self.spacing

        self.total_width = total_width

        match self.align:
            case AlignEnum.LEFT:
                cursor_x = self.position.x
            case AlignEnum.RIGHT:
                cursor_x = self.position.x - total_width
            case _:
                cursor_x = round(self.position.x - total_width / 2)
        for index, character in enumerate(self.text):
            infos = self.font.get_characters()[character]
            character_position = Position(
                round(cursor_x + infos["bearing_x"]),
                round(self.position.y - infos["bearing_y"]),
            )

            if index < len(self.characters):
                mesh = self.characters[index]
                mesh.character = character
                mesh.infos = infos
                mesh.position = character_position
                mesh.set_color(self.get_color())
                mesh.set_operation(self.get_operation())
                mesh.set_scale(self.scale)
            else:
                mesh = Character(
                    character,
                    infos,
                    self.get_color(),
                    character_position,
                    operation=self.get_operation(),
                )
                self.characters.append(mesh)
                self.layer.meshes.append(mesh)

            cursor_x += infos["advance"] + self.spacing

    def set_scale(self, scale: float) -> None:
        """
        Assign the scale.

        Args:
            scale: Scale used by the operation.
        """
        self.scale = scale
        for character in self.characters:
            character.set_scale(scale)

    def refresh(self) -> None:
        """
        Refresh the rendered state.
        """
        self.set_sequence_text(self.text)

    def get_layer(self) -> MeshLayer:
        """
        Return the current layer.

        Returns:
            The current layer.
        """
        return self.layer
