from dataclasses import dataclass

from src.texture.frame import Frame


@dataclass(frozen=True)
class AnimationDef:
    frames: tuple['Frame | AnimationDef', ...]
    duration: float
    loop: bool = True
