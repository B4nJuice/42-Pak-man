import moderngl

from src.errors import GlContextError, GlTextureNotUpload

from .image_data import ImageData


class GLTexture:
    ctx: moderngl.Context | None = None

    _tex: moderngl.Texture | None
    _pixel_art: bool
    _mipmaps: bool
    _anisotropy: float
    def __init__(
                self,
                data: ImageData,
                *,
                pixel_art: bool = True,
                mipmaps: bool | None = None,
                anisotropy: float = 1.0
            ) -> None:

        self._tex = None
        self._pixel_art = pixel_art
        self._mipmaps = (not pixel_art) if mipmaps is None else mipmaps
        self._anisotropy = anisotropy
        self.upload(data)

    @property
    def width(self) -> int:
        if self._tex is None:
            raise GlTextureNotUpload()
        return self._tex.width

    @property
    def height(self) -> int:
        if self._tex is None:
            raise GlTextureNotUpload()
        return self._tex.height

    def upload(self, data: ImageData) -> None:
        if self.ctx is None:
            raise GlContextError()
        size = (data.width, data.height)
        if self._tex is None or self._tex.size != size:
            self.destroy()
            self._tex = self.ctx.texture(size, 4, data.pixels)
            self._tex.repeat_x = self._tex.repeat_y = False
            self._tex.anisotropy = self._anisotropy
            if self._pixel_art:
                f = moderngl.NEAREST_MIPMAP_NEAREST if self._mipmaps else moderngl.NEAREST
                self._tex.filter = (f, moderngl.NEAREST)
            else:
                f = moderngl.LINEAR_MIPMAP_LINEAR if self._mipmaps else moderngl.LINEAR
                self._tex.filter = (f, moderngl.LINEAR)
        else:
            self._tex.write(data.pixels)
        if self._mipmaps:
            self._tex.build_mipmaps()

    def bind(self, unit: int = 0) -> None:
        if self._tex is None:
            raise GlTextureNotUpload()
        self._tex.use(unit)

    def destroy(self) -> None:
        if self._tex is not None:
            self._tex.release()
            self._tex = None
