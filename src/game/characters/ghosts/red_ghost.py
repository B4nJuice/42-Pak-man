from src.core.level import Level
from src.utils import Direction

from ..ghost import Ghost


class RedGhost(Ghost):
    def __init__(self, id: int, level: Level) -> None:
        self._texture_path = 'assets/characters/ghosts/red'

        super().__init__(f'red_ghost_{id}', (0, 0), level)

        self.add_next_move(Direction.EAST)
        self.add_next_move(Direction.SOUTH)
        self.add_next_move(Direction.EAST)
