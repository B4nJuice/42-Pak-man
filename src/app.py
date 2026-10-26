from dataclasses import dataclass
from typing import TYPE_CHECKING

from moderngl import Context

from src.config import ConfigManager
from src.texture import TextureManager
from src.utils.size import SizeCore

if TYPE_CHECKING:
    from src.fonts.font_manager import FontManager

@dataclass(frozen=True)
class App:
    ctx: Context
    config: ConfigManager
    texture: TextureManager
    size: SizeCore
    fonts: 'FontManager'
