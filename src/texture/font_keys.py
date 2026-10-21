from enum import Enum

from src.errors.pack_invalid_key import PackInvalidKey


class FontKeys(Enum):
    DEFAULT = 'default'

    @classmethod
    def get(cls, key: str) -> 'FontKeys':
        entry: FontKeys | None = next(
            (member for member in cls if member.value == key),
            None
        )
        if entry is None:
            raise PackInvalidKey(key)
        return entry
