from pathlib import Path

from src.errors.base_error import BaseError


class MissingTexturesError(BaseError):
    def __init__(self, paths: list[Path]) -> None:
        """
        Initialize the instance.

        Args:
            paths: Paths used by the operation.
        """
        super().__init__(
            f'Missing textures : {[path.as_posix() for path in paths]}'
        )
