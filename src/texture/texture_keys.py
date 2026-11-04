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

    MAIN_BACKDROP = 'main-backdrop'
    LOBBY_ASSETS_PACMAN_GHOST = 'lobby-assets-pacman-ghost'
    VICTORY_PACMAN = 'victory-pacman'
    GAMEOVER_GHOST = 'gameover-ghost'

    HOW_TO_PLAY_01 = 'how-to-play-01'
    HOW_TO_PLAY_02 = 'how-to-play-02'
    HOW_TO_PLAY_03 = 'how-to-play-03'
    HOW_TO_PLAY_04 = 'how-to-play-04'

    @classmethod
    def get(cls, key: str) -> 'TextureKeys':
        entry: TextureKeys | None = next(
            (member for member in cls if member.value == key),
            None
        )
        if entry is None:
            raise PackInvalidKey(key)
        return entry

    def str(self) -> str:
        return self.value
