from dataclasses import dataclass

from src.texture.animation_definition import AnimationDef


@dataclass(frozen=True)
class TextureDef:
    variants: dict[str, AnimationDef]
    default_variant: str
