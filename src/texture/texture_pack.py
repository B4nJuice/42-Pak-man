import json
from dataclasses import dataclass
from pathlib import Path

from src.errors import PackError
from src.texture.texture_keys import TextureKeys
from src.utils import Logger, TColor

logger = Logger(name='Texture', color=TColor.CYAN, verbose=True)

DEFAULT_VARIANT = 'default'
DEFAULT_FRAME_TIME = 0.1
MAX_FRAMES = 256

@dataclass(frozen=True)
class Frame:
    path: Path
    duration: float

@dataclass(frozen=True)
class AnimationDef:
    frames: tuple['Frame | AnimationDef', ...]
    loop: bool = True

@dataclass(frozen=True)
class TextureDef:
    variants: dict[str, AnimationDef]
    default_variant: str


class TexturePack:
    root: Path
    name: str
    _textures: dict[TextureKeys, TextureDef]

    def __init__(self, root: Path, name: str, textures: dict[TextureKeys, TextureDef]):
        self.root = root
        self.name = name
        self._textures = textures

    @classmethod
    def from_directory(cls, root: str | Path) -> 'TexturePack':
        root = Path(root).resolve()
        manifest = root / 'pack.json'

        if not root.is_dir():
            raise PackError(f'Pack directory not found: {root}')
        if not manifest.is_file():
            raise PackError(f'Missing pack.json in {root}')
        try:
            data = json.loads(manifest.read_text(encoding='utf-8'))
            raw_textures = data['textures']
            if not isinstance(raw_textures, dict):
                raise TypeError('\'textures\' must be an object')
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            raise PackError(f'Invalid manifest in {root}: {e}') from e

        textures = {}
        for texture_key, raw in raw_textures.items():
            try:
                textures[texture_key] = cls._parse_texture(root, raw)
            except (PackError, KeyError, TypeError, ValueError, AttributeError) as e:
                logger.warning(f'Texture {texture_key!r} in {root.name} ignored: {e}')
        return cls(root, data.get('name', root.name), textures)

    def get(self, key: TextureKeys) -> TextureDef:
        return self._textures.get(key)

    @staticmethod
    def _parse_texture(root: Path, raw: dict | str | list, inherit: dict) -> dict[TextureKeys, TextureDef]:
        pass
