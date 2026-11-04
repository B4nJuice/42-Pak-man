from enum import Enum


class GameStatus(Enum):
    EXIT = -1
    RUNNING = 0
    PAUSED = 1
    INITIALIZING = 2
    AMELIORATION = 3
    CHEAT_MENU = 4

    @classmethod
    def get_all(cls) -> list["GameStatus"]:
        return [status for status in cls]
