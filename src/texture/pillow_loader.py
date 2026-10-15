from pathlib import Path

from PIL import Image

from .image_data import ImageData
from .texture_loader import MAX_DIM, TextureLoader


class PillowLoader(TextureLoader):
    def load(self, path: Path) -> ImageData:
        with Image.open(path) as im:
            im.load()
            if max(im.size) > MAX_DIM:
                raise ValueError(f"image too large: {im.size}")
            im = im.convert("RGBA")
            im = im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

            return ImageData(im.width, im.height, im.tobytes())
