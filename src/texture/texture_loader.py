from pathlib import Path

import moderngl
from moderngl import Context
from PIL import Image

from src.errors import AssetLoadError

from .texture_data import TextureData

MAX_DIM = 4096


class TextureLoader:
    _ctx: Context
    _textures: dict[Path, TextureData]

    def __init__(self, ctx: Context) -> None:
        """
        Initialize the instance.

        Args:
            ctx: Ctx used by the operation.
        """
        self._ctx = ctx
        self._textures = {}

    def load(self, path: Path) -> TextureData:
        """
        Load the associated data.

        Args:
            path: Filesystem path used to load or save the data.

        Returns:
            The value produced by the load operation.
        """
        if path in self._textures:
            return self._textures[path]

        try:
            with Image.open(path) as im:
                im.load()
                if max(im.size) > MAX_DIM:
                    raise ValueError(f'image too large: {im.size}')
                image = im.convert('RGBA')

                texture = self._ctx.texture(image.size, 4, image.tobytes())
                texture.filter = (
                    moderngl.NEAREST,
                    moderngl.NEAREST,
                )
                texture.use(location=0)

                self._textures[path] = TextureData(texture, image.size)
                return self._textures[path]
        except (OSError, ValueError, RuntimeError) as exc:
            raise AssetLoadError(
                path,
                pack=str(path.parent),
                reason=str(exc),
            ) from exc

    def unload(self, path: Path) -> None:
        """
        Handle unload.

        Args:
            path: Filesystem path used to load or save the data.
        """
        if path not in self._textures:
            return

        self._textures[path].texture.release()
        del self._textures[path]

    def get(self, path: Path) -> TextureData:
        """
        Handle get.

        Args:
            path: Filesystem path used to load or save the data.

        Returns:
            The value produced by the get operation.
        """
        return self._textures[path]
