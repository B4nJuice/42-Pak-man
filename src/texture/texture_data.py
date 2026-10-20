from dataclasses import dataclass

from moderngl import Texture


@dataclass(frozen=True)
class TextureData:
    texture: Texture
    size: tuple[int, int]

    @property
    def width(self) -> int:
        return self.size[0]

    @property
    def height(self) -> int:
        return self.size[1]
