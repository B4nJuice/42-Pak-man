from src.core import AStar, Level, Tile

# from src.utils import Direction
from ..ghost import Ghost
from ..player import Player


class RedGhost(Ghost):
    a_star: AStar
    # next_update_in: float

    def __init__(self, id: int, level: Level) -> None:
        self._texture_path = 'assets/characters/ghosts/red'
        self.a_star = AStar(level)

        super().__init__(f'red_ghost_{id}', (0, 0), level)

        player = self.level.entities.get(Player)[0]

        if not player:
            return

        self.go_to(player.get_tile())

    def go_to(self, tile: Tile) -> None:
        path = self.a_star.find_path(
            start=self.get_tile(),
            end=tile
        )

        self.clear_next_moves()
        for _, direction in path:
            print(direction)
            self.add_next_move(direction)
