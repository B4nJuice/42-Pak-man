from enum import Enum


class GameState(Enum):
    EXIT = -1
    RUNNING = 0
    PAUSED = 1
    INITIALIZING = 2
