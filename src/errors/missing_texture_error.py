
from src.errors.base_error import BaseError


class MissingTextureError(BaseError):
    def __init__(self) -> None:
        super().__init__('Missing textures in base texture pack')
