import freetype
from moderngl import Context

class Font:
    def __init__(
                self,
                font_path: str,
                context: Context,
                pixel_size: int = 48
            ) -> None:
        self.font_path: str = font_path
        self.context: Context = context

        self.characters = {}

        self.face: freetype.Face = freetype.Face(self.font_path)
        self.face.set_pixel_sizes(0, pixel_size)

        for char in range(32, 127):
            self.face.load_char(chr(char))

            glyph = self.face.glyph
            bitmap = glyph.bitmap

            texture: Context.texture = self.context.texture(
                (bitmap.width, bitmap.rows),
                1,
                bytes(bitmap.buffer),
            )

            self.characters[chr(char)] = {
                "texture": texture,
                "width": bitmap.width,
                "height": bitmap.rows,
                "bearing_x": glyph.bitmap_left,
                "bearing_y": glyph.bitmap_top,
                "advance": glyph.advance.x >> 6,
            }
