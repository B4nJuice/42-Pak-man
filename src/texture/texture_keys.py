from enum import Enum

from src.errors import PackInvalidKey


class TextureKeys(Enum):
    PACGUM = 'pacgum'
    SUPER_PACGUM = 'super-pacgum'

    PACMAN = 'pacman'

    GHOST_BLINKY = 'ghost-blinky'
    GHOST_PINKY = 'ghost-pinky'
    GHOST_INKY = 'ghost-inky'
    GHOST_CLYDE = 'ghost-clyde'

    GHOST_EATEN = 'ghost-eaten'
    GHOST_FRIGHTENED = 'ghost-frightened'

    AMELIORATION_UNKNOWN = 'amelioration-unknown'
    AMELIORATION_EXP = 'amelioration-exp'
    AMELIORATION_LUCK = 'amelioration-luck'
    AMELIORATION_POWER = 'amelioration-power'
    AMELIORATION_SPEED = 'amelioration-speed'
    AMELIORATION_SUPER_TIME = 'amelioration-super-time'

    @classmethod
    def get(cls, key: str) -> 'TextureKeys':
        entry: TextureKeys | None = next(
            (member for member in cls if member.value == key),
            None
        )
        if entry is None:
            raise PackInvalidKey(key)
        return entry
