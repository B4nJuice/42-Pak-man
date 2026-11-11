from dataclasses import dataclass

from moderngl import Texture


@dataclass(frozen=True)
class TextureData:
    texture: Texture
    size: tuple[int, int]

    @property
    def width(self) -> int:
        """
        Handle width.

        Returns:
            The value produced by the width operation.
        """
        return self.size[0]

    @property
    def height(self) -> int:
        """
        Handle height.

        Returns:
            The value produced by the height operation.
        """
        return self.size[1]
