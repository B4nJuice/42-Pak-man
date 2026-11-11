from dataclasses import dataclass


@dataclass(frozen=True)
class ImageData:
    size: tuple[int, int]
    pixels: bytes

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
