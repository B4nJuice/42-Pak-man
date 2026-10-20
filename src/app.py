from dataclasses import dataclass

from moderngl import Context

from src.config import ConfigManager
from src.texture import TextureManager


@dataclass(frozen=True)
class App:
    ctx: Context
    config: ConfigManager
    texture: TextureManager
