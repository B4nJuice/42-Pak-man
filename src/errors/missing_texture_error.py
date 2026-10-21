from src.errors.base_error import BaseError


class MissingTextureError(BaseError):
    def __init__(self, missing: list[str] | None = None) -> None:
        if missing is None:
            super().__init__('Missing textures in base texture pack. Please restore \'assets\' folder !')
            return
        joined = ', '.join(repr(key) for key in missing)
        super().__init__(f'Missing textures in base texture pack: {joined}. Please restore \'assets\' folder !')
