from src.texture.texture_keys import TextureKeys
from src.texture.texture_loader import TextureLoader
from src.texture.texture_pack import TexturePack


class TextureManager:
    _loader: TextureLoader
    _default_path: str

    _default: TexturePack
    _user: TexturePack | None

    def __init__(self, texture_loader: TextureLoader, default_path: str) -> None:
        self._loader = texture_loader
        self._default_path = default_path

        self._default = TexturePack.from_directory(default_path)
        self._user = None

    def load_pack(self, path: str) -> None:
        # raise ValueError('TODO: to implement')

    # def get(self, key: TextureKeys, variant: str | None = None) -> Animation:
        