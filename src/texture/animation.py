from dataclasses import dataclass

from .texture_frame import TextureFrame


@dataclass(frozen=True)
class Animation:
    frames: list['Animation | TextureFrame']
    duration: float
    loop: bool = True
