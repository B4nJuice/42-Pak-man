from dataclasses import dataclass


@dataclass(frozen=True)
class ImageData:
    width: int
    height: int
    pixels: bytes

    @property
    def size(self) -> tuple[int, int]:
        return (self.width, self.height)
