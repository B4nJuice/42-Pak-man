from PIL import Image

from src.graphics import Mesh, Color, OperationEnum, Position

class ImageTexture(Mesh):
    def __init__(
                self,
                path: str,
                position: Position,
                operation: OperationEnum = OperationEnum.SET,
                is_dynamic: bool = False
            ) -> None:
        super().__init__(
                Color.default(),
                operation,
                is_dynamic
            )

        self.position: Position = position
        self.path: str = path
        self.image: Image = Image.open(self.path).convert("RGBA")
