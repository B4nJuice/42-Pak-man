from PIL import Image
from typing import Any

from ..color import Color, OperationEnum
from ..mesh import Mesh
from ..position import Position


class ImageTexture(Mesh):
    position: Position
    path: str
    image: Image.Image
    original_width: int
    original_height: int
    width: int
    height: int
    texture: Any

    def __init__(
                self,
                path: str,
                position: Position,
                width: int = 0,
                height: int = 0,
                operation: OperationEnum = OperationEnum.SET,
                dynamic: bool = False
            ) -> None:
        super().__init__(
            Color.default(),
            operation,
            dynamic
        )

        self.position = position
        self.path = path
        self.image = Image.open(self.path).convert("RGBA")
        self.original_width, self.original_height = self.image.size
        self.width = width or self.original_width
        self.height = height or self.original_height
        self.texture = None

    def get_position(self) -> Position:
        return self.position

    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height

    @classmethod
    def create_blank(cls, path: str) -> 'ImageTexture':
        return cls(
            path=path,
            position=Position(0, 0),
            width=0,
            height=0,
            operation=OperationEnum.SET,
            dynamic=False,
        )
