from abc import ABC
from pathlib import Path

import moderngl
from moderngl import Context, create_context
from PIL import Image

from .texture_data import TextureData

MAX_DIM = 4096


class TextureLoader(ABC):
    _ctx: Context

    def __init__(self) -> None:
        self._ctx = create_context()
        self._textures = {}

    def load(self, path: Path) -> TextureData:
        if path in self._textures:
            return self._textures[path]

        with Image.open(path) as im:
            im.load()
            if max(im.size) > MAX_DIM:
                raise ValueError(f'image too large: {im.size}')
            im = im.convert('RGBA')
            im = im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

            texture = self._ctx.texture(im.size, 4, im.tobytes())
            texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
            texture.use(location=0)

            self._textures[path] = TextureData(texture, im.size)
            return self._textures[path]

    def unload(self, path: Path) -> None:
        if not path in self._textures:
            return

        self._textures[path].texture.release()
        del self._textures[path]

    def get(self, path: Path) -> TextureData:
        return self._textures[path]
