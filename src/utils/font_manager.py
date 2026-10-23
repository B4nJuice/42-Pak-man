from enum import Enum

from freetype.ft_errors import FT_Exception
from moderngl import Context

from src.errors import WrongFontFormatError
from src.graphics.font.font import Font
from src.texture import TextureManager
from src.texture.font_keys import FontKeys

from .size import SizeCore


class FontKey(Enum):
    TEXT_8 = (8, FontKeys.DEFAULT)
    BOLD_8 = (8, FontKeys.BOLD)
    BOLD_10 = (10, FontKeys.BOLD)
    BOLD_18 = (18, FontKeys.BOLD)
    BOLD_24 = (24, FontKeys.BOLD)
    TITLE_10 = (10, FontKeys.TITLE)
    TITLE_14 = (14, FontKeys.TITLE)
    TITLE_24 = (24, FontKeys.TITLE)
    TITLE_36 = (36, FontKeys.TITLE)
    TITLE_40 = (40, FontKeys.TITLE)

    def __init__(self, size: int, style: FontKeys):
        self.size = size
        self.style = style


class FontManager:
    _sizes: SizeCore
    _texture_manager: TextureManager
    _context: Context
    _fonts: dict[FontKey, Font]

    def __init__(
                self,
                sizes: SizeCore,
                texture_manager: TextureManager,
                context: Context
            ) -> None:
        self._sizes = sizes
        self._texture_manager = texture_manager
        self._context = context

        self.calculate()

    def get(self, key: FontKey) -> Font:
        return self._fonts[key]

    def calculate(self) -> None:
        self._fonts = {}

        for font_key in FontKey:
            font_path = self._texture_manager.get_font(
                font_key.style
            ).as_posix()

            try:
                self._fonts[font_key] = Font(
                    font_path=font_path,
                    context=self._context,
                    pixel_size=self._sizes.get(font_key.size),
                )
            except FT_Exception as exp:
                raise WrongFontFormatError(font_path) from exp
