from src.graphics import SuperMesh, Color, OperationEnum, Position, MeshLayer
from src.graphics.meshes import Character
from src.graphics.font import Font

class FontSequence(SuperMesh):
    def __init__(
                self,
                text: str,
                font: Font,
                color: Color,
                position: Position,
                spacing: int = 0,
                operation: OperationEnum = OperationEnum.SET,
                is_dynamic: bool = False
            ) -> None:
        super().__init__(
                color,
                operation,
                is_dynamic
            )

        self.font: Font = font
        self.position: Position = position
        self.spacing: int = spacing
        self.layer: MeshLayer = MeshLayer()
        self.characters: list[Character] = []
        self.init()
        self.set_sequence_text(text)

    def init(self) -> None:
        pass

    def set_sequence_text(self, text: str) -> None:
        self.text: str = text
        if len(self.characters) != len(text):
            self.characters = []
            self.layer.meshes.clear()

        cursor_x = self.position.x
        for index, character in enumerate(self.text):
            infos = self.font.characters[character]
            character_position = Position(
                cursor_x + infos["bearing_x"],
                self.position.y - infos["bearing_y"],
            )

            if index < len(self.characters):
                mesh = self.characters[index]
                mesh.character = character
                mesh.infos = infos
                mesh.position = character_position
                mesh.color = self.color
                mesh.operation = self.operation
            else:
                mesh = Character(
                    character,
                    infos,
                    self.color,
                    character_position,
                    operation=self.operation,
                    is_dynamic=self.is_dynamic,
                )
                self.characters.append(mesh)
                self.layer.meshes.append(mesh)

            cursor_x += infos["advance"] + self.spacing

    def refresh(self) -> None:
        self.set_sequence_text(self.text)

    def get_layer(self) -> MeshLayer:
        return self.layer
