from abc import ABC, abstractmethod
from pathlib import Path

from moderngl import Texture

from .image_data import ImageData

MAX_DIM = 4096

class TextureLoader(ABC):
    _texures: dict[Path, Texture]

    def __init__(self)

    @abstractmethod
    def load(self, path: Path) -> ImageData:
        pass
