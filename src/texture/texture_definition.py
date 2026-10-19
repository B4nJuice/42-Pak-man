from dataclasses import dataclass

from src.texture.animation import Animation
from src.texture.animation_definition import AnimationDef


@dataclass(frozen=True)
class TextureDef:
    variants: dict[str, AnimationDef]
    default_variant: str

@dataclass(frozen=True)
class Texture:
    variants: dict[str, Animation]
    default_variant: str