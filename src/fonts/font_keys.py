from enum import Enum

from src.errors.pack_invalid_key import PackInvalidKey


class FontKeys(Enum):
    DEFAULT = 'default'
    BOLD = 'default-bold'
    TITLE = 'title'
    TITLE_SECONDARY = 'title-secondary'

    @classmethod
    def get(cls, key: str) -> 'FontKeys':
        """
        Handle get.

        Args:
            key: Keyboard key code associated with the action.

        Returns:
            The value produced by the get operation.
        """
        entry: FontKeys | None = next(
            (member for member in cls if member.value == key),
            None
        )
        if entry is None:
            raise PackInvalidKey(key)
        return entry
