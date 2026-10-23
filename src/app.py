from dataclasses import dataclass

from moderngl import Context

from src.config import ConfigManager
from src.texture import TextureManager
from src.utils.font_manager import FontManager
from src.utils.size import SizeCore


@dataclass(frozen=True)
class App:
    ctx: Context
    config: ConfigManager
    texture: TextureManager
    size: SizeCore
    fonts: FontManager
