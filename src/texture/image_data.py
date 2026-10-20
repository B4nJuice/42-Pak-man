from dataclasses import dataclass


@dataclass(frozen=True)
class ImageData:
    size: tuple[int, int]
    pixels: bytes

    @property
    def width(self) -> int:
        return self.size[0]

    @property
    def height(self) -> int:
        return self.size[1]
