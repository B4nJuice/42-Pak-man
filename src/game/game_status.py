from enum import Enum


class GameStatus(Enum):
    EXIT = -1
    RUNNING = 0
    PAUSED = 1
    INITIALIZING = 2
    AMELIORATION = 3
