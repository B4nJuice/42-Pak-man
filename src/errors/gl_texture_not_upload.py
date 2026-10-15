from src.errors.base_error import BaseError


class GlTextureNotUpload(BaseError):
    def __init__(self) -> None:
        super().__init__('Texture not uploaded')
