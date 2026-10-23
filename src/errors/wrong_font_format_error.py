from src.errors.base_error import BaseError


class WrongFontFormatError(BaseError):
    def __init__(self, file: str) -> None:
        super().__init__(
            f'Invalid font format for file {file!r}. '
            'Please provide a supported font file (ttf) !'
        )
