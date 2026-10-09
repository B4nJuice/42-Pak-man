from PIL import Image

from ..color import Color, OperationEnum
from ..mesh import Mesh
from ..position import Position


class ImageTexture(Mesh):
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

        self.position: Position = position
        self.path: str = path
        self.image: Image.Image = Image.open(self.path).convert("RGBA")
        self.original_width, self.original_height = self.image.size
        self.width: int = width or self.original_width
        self.height: int = height or self.original_height
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
