import json
from pathlib import Path
from typing import Any

from src.errors import PackError
from src.fonts import FontKeys
from src.texture.animation_definition import AnimationDef
from src.texture.frame import Frame
from src.texture.texture_definition import TextureDef
from src.texture.texture_keys import TextureKeys
from src.utils import Logger, TColor, is_list_of

TRAW = str | list[str] | dict[str, Any]

DEFAULT_VARIANT: str = 'default'
DEFAULT_FRAME_TIME: float = 0.1
MAX_FRAMES: int = 256

LOGGER: Logger = Logger(name='Texture', color=TColor.CYAN, verbose=True)


class TexturePack:
    root: Path
    name: str
    _textures: dict[TextureKeys, TextureDef]
    _fonts: dict[FontKeys, Path]

    def __init__(
                self,
                root: Path,
                name: str,
                textures: dict[TextureKeys, TextureDef],
                fonts: dict[FontKeys, Path]
            ) -> None:
        self.root = root
        self.name = name
        self._textures = textures
        self._fonts = fonts

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
            raw_fonts = data['fonts']
            if not isinstance(raw_textures, dict):
                raise TypeError('\'textures\' must be an object')
            if not isinstance(raw_fonts, dict):
                raise TypeError('\'fonts\' must be an object')
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            raise PackError(f'Invalid manifest in {root}: {e}') from e

        textures: dict[TextureKeys, TextureDef] = {}
        for texture_key, raw in raw_textures.items():
            try:
                textures[TextureKeys.get(texture_key)] = cls._parse_texture(
                    root,
                    raw,
                )
            except (
                PackError,
                KeyError,
                TypeError,
                ValueError,
                AttributeError,
            ) as e:
                LOGGER.warning(
                    f'Texture {texture_key!r} in {root.name} ignored: {e}'
                )

        fonts: dict[FontKeys, Path] = {}
        for font_key, raw in raw_fonts.items():
            try:
                fonts[FontKeys.get(font_key)] = cls._parse_font(root, raw)
            except (
                PackError,
                KeyError,
                TypeError,
                ValueError,
                AttributeError,
            ) as e:
                LOGGER.warning(
                    f'Font {font_key!r} in {root.name} ignored: {e}'
                )

        return cls(root, data.get('name', root.name), textures, fonts)

    def get(self, key: TextureKeys) -> TextureDef | None:
        return self._textures.get(key)

    def get_font(self, key: FontKeys) -> Path | None:
        return self._fonts.get(key)

    @staticmethod
    def _parse_font(root: Path, raw: Any) -> Path:
        if not isinstance(raw, str):
            raise PackError(
                f'font element must be a string, found: {type(raw)!r}'
            )
        return TexturePack._safe_path(root, raw)

    @staticmethod
    def _parse_texture(root: Path, raw: TRAW) -> TextureDef:
        if isinstance(raw, dict) and 'variants' in raw:
            inherit = {k: raw[k] for k in ('frame_time', 'loop') if k in raw}
            variants = {
                key: TexturePack._parse_animation_raw(root, v_raw, inherit)
                for key, v_raw in raw['variants'].items()
            }
            default_variant: str = raw.get('default_variant', DEFAULT_VARIANT)

            if default_variant not in variants:
                raise PackError(
                    f'No default variant {default_variant!r} defined for '
                    f'texture; available variants: {tuple(variants.keys())}'
                )

            return TextureDef(
                variants=variants,
                default_variant=default_variant
            )

        return TextureDef(
            variants={
                DEFAULT_VARIANT: (
                    TexturePack._parse_animation_raw(root, raw, {})
                )
            },
            default_variant=DEFAULT_VARIANT
        )

    @staticmethod
    def _parse_animation_raw(
                root: Path,
                raw: TRAW,
                inherit: dict
            ) -> AnimationDef:
        frame_time: float
        loop: bool

        if isinstance(raw, dict):
            frame_time = float(raw.get(
                'frame_time',
                inherit.get('frame_time', DEFAULT_FRAME_TIME))
            )
            loop = bool(raw.get('loop', inherit.get('loop', True)))
        else:
            frame_time = float(inherit.get('frame_time', DEFAULT_FRAME_TIME))
            loop = bool(inherit.get('loop', True))

        if isinstance(raw, str):
            return TexturePack._parse_animation(root, [raw], frame_time, loop)
        elif isinstance(raw, list):
            return TexturePack._parse_animation(root, raw, frame_time, loop)
        elif isinstance(raw, dict) and 'frames' in raw \
                and isinstance(raw['frames'], list):
            if is_list_of(raw['frames'], str):
                return TexturePack._parse_animation(
                    root,
                    raw['frames'],
                    frame_time,
                    loop
                )
            else:
                frames: list[AnimationDef] = []
                for item in raw['frames']:
                    frames.append(TexturePack._parse_animation_raw(
                        root,
                        item,
                        {'frame_time': frame_time, 'loop': loop}
                    ))
                return AnimationDef(
                    frames=tuple(frames),
                    loop=loop,
                    duration=frame_time
                )
        elif isinstance(raw, dict) and 'file' in raw:
            return TexturePack._parse_animation(root, [raw], frame_time, loop)
        else:
            raise PackError('animation must be a string, list or object')

    @staticmethod
    def _parse_animation(
                root: Path,
                items: list[str] | list[dict[str, str]],
                frame_time: float,
                loop: bool
            ) -> AnimationDef:
        if not isinstance(items, list) or not 0 < len(items) <= MAX_FRAMES:
            raise PackError(
                f'\'frames\' must be a list of 1..{MAX_FRAMES} entries'
            )

        frames = []
        for item in items:
            if isinstance(item, str):
                file, duration = item, frame_time
            elif isinstance(item, dict):
                file, duration = item['file'], float(item.get(
                    'duration',
                    frame_time
                ))
            else:
                raise PackError(f'invalid frame entry: {item!r}')
            if not 0 < duration < 3600:
                raise PackError(f'invalid duration: {duration}')
            frames.append(Frame(TexturePack._safe_path(root, file), duration))
        return AnimationDef(
            frames=tuple(frames),
            loop=loop,
            duration=frame_time
        )

    @staticmethod
    def _safe_path(root: Path, rel: str) -> Path:
        path = (root / rel).resolve()
        if root not in path.parents:
            raise PackError(f'path escapes pack: {rel!r}')
        if not path.exists():
            raise PackError(f'file not found: {rel!r}')
        return path
