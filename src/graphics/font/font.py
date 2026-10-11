import freetype
from typing import Any
from moderngl import Context


class Font:
    _font_path: str
    _context: Context
    _characters: dict[str, Any]
    _face: freetype.Face

    def __init__(
                self,
                font_path: str,
                context: Context,
                pixel_size: int = 48
            ) -> None:
        self._font_path = font_path
        self._context = context

        self._characters = {}

        self._face = freetype.Face(self._font_path)
        self._face.set_pixel_sizes(0, pixel_size)

        for char in range(32, 127):
            self._face.load_char(chr(char))

            glyph = self._face.glyph
            bitmap = glyph.bitmap

            texture: Context.texture = self._context.texture(
                (bitmap.width, bitmap.rows),
                1,
                bytes(bitmap.buffer),
            )

            self._characters[chr(char)] = {
                "texture": texture,
                "width": bitmap.width,
                "height": bitmap.rows,
                "bearing_x": glyph.bitmap_left,
                "bearing_y": glyph.bitmap_top,
                "advance": glyph.advance.x >> 6,
            }

    def get_characters(self) -> dict[str, Any]:
        return self._characters
