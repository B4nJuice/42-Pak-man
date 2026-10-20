from src.errors import MissingTextureError
from src.texture.animation import Animation
from src.texture.animation_definition import AnimationDef
from src.texture.frame import Frame
from src.texture.texture_definition import Texture
from src.texture.texture_frame import TextureFrame
from src.texture.texture_keys import TextureKeys
from src.texture.texture_loader import TextureLoader
from src.texture.texture_pack import TexturePack


class TextureManager:
    _loader: TextureLoader

    _default: TexturePack
    _user: TexturePack | None

    _textures: dict[TextureKeys, Texture]

    def __init__(self, texture_loader: TextureLoader, default_path: str) -> None:
        self._loader = texture_loader

        self._default = TexturePack.from_directory(default_path)
        self._user = None

        self._textures = {}
        self.load_textures(self._default)

    def load_pack(self, path: str) -> None:
        raise ValueError('TODO: to implement')

    def get(self, key: TextureKeys, variant: str | None = None) -> Animation:
        texture: Texture = self._textures[key]

        if variant is None or variant not in texture.variants:
            return texture.variants[texture.default_variant]
        else:
            return self._textures[key].variants[variant]

    def load_textures(self, pack: TexturePack) -> None:
        _missing_textures: list[TextureKeys] = []

        for key in TextureKeys:
            texture_definition = pack.get(key)
            if texture_definition is None:
                _missing_textures.append(key)
                continue

            variants: dict[str, Animation] = {}
            for variant_key, variant in texture_definition.variants.items():
                variants[variant_key] = self._transform_animation(variant)

            self._textures[key] = Texture(
                default_variant=texture_definition.default_variant,
                variants=variants
            )

        if pack == self._default and len(_missing_textures) > 0:
            raise MissingTextureError()

    def _transform_animation(self, definition: AnimationDef) -> Animation:
        return Animation(
            frames=[
                self._build_frame(frame)
                for frame in definition.frames
            ],
            duration=definition.duration,
            loop=definition.loop
        )

    def _build_frame(self, frame: Frame | AnimationDef) -> Animation | TextureFrame:
        if isinstance(frame, AnimationDef):
            return self._transform_animation(frame)
        data = self._loader.load(frame.path)
        return TextureFrame(
            texture=data.texture,
            size=data.size,
            path=frame.path,
            duration=frame.duration,
        )
