from src.errors.base_error import BaseError


class WrongFontFormatError(BaseError):
    def __init__(self, file: str) -> None:
        """
        Initialize the instance.

        Args:
            file: File used by the operation.
        """
        super().__init__(
            f'Invalid font format for file {file!r}. '
            'Please provide a supported font file (ttf) !'
        )
