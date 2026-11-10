from enum import Enum


class GameStatus(Enum):
    EXIT = -1
    IDLE = 0
    RUNNING = 1
    PAUSED = 2
    INITIALIZING = 3
    AMELIORATION = 4
    VICTORY = 5
    GAMEOVER = 6
    CHEAT_MENU = 7

    @classmethod
    def get_all(cls) -> list["GameStatus"]:
        return [status for status in cls]


class InterfaceStatus(Enum):
    RUNNING = 0
    PAUSED = 1
    INITIALIZING = 2
    AMELIORATION = 3
    CHEAT_MENU = 4
    VICTORY = 5
    GAMEOVER = 6
    HOWTOPLAY = 7
    LEADERBOARD = 8
    SETTINGS = 9
    LOBBY = 10
    SAVE_RUN = 11

    @classmethod
    def get_all(cls) -> list["InterfaceStatus"]:
        return [status for status in cls]
