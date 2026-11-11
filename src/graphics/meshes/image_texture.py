from typing import Any

from PIL import Image

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
            ) -> None:
        """
        Initialize the instance.

        Args:
            path: Filesystem path used to load or save the data.
            position: Screen or world coordinates of the object.
            width: Width of the screen or rendered element.
            height: Height of the screen or rendered element.
            operation: Operation used by the operation.
        """
        super().__init__(
            Color.default(),
            operation,
        )

        self.position = position
        self.path = path
        self.image = Image.open(self.path).convert("RGBA")
        self.original_width, self.original_height = self.image.size
        self.width = width or self.original_width
        self.height = height or self.original_height
        self.texture = None

    def get_position(self) -> Position:
        """
        Return the current position.

        Returns:
            The current position.
        """
        return self.position

    def get_width(self) -> int:
        """
        Return the current width.

        Returns:
            The current width.
        """
        return self.width

    def get_height(self) -> int:
        """
        Return the current height.

        Returns:
            The current height.
        """
        return self.height

    @classmethod
    def create_blank(cls, path: str) -> 'ImageTexture':
        """
        Handle create blank.

        Args:
            path: Filesystem path used to load or save the data.

        Returns:
            The value produced by the create blank operation.
        """
        return cls(
            path=path,
            position=Position(0, 0),
            width=0,
            height=0,
            operation=OperationEnum.SET,
        )
