from PIL import Image

from src.graphics import Color, Mesh, OperationEnum, Position


class ImageTexture(Mesh):
    def __init__(
                self,
                path: str,
                position: Position,
                width: int = 0,
                height: int = 0,
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
        self.image: Image.Image = Image.open(self.path).convert("RGBA")
        self.original_width, self.original_height = self.image.size
        self.width: int = width or self.original_width
        self.height: int = height or self.original_height
        self.texture = None
