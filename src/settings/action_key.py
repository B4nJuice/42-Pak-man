from enum import Enum, auto


class ActionKey(Enum):
    MOVE_UP = auto()
    MOVE_DOWN = auto()
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    SELECT = auto()
    BACK_PAUSE_RESUME = auto()
