from dataclasses import dataclass

from .frame import Frame
from .texture_data import TextureData


@dataclass(frozen=True)
class TextureFrame(Frame, TextureData):
     pass
