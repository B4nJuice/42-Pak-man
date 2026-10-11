from src.core import Level, Tile
from src.utils import Pos
from random import randint

from ..ghost import Ghost


class ClydeGhost(Ghost):

    def __init__(self, id: int, tile: Pos | Tile, level: Level) -> None:
        self._texture_path = 'assets/characters/ghosts/orange'

        super().__init__(
            name=f'clyde_ghost_{id}',
            tile=tile,
            level=level,
            update_tracking_interval=-1
        )

    def get_tracking_tile(self) -> Tile:
        width = self.level.get_width()
        height = self.level.get_height()
        perimeter = 2 * width + 2 * height - 4
        tile_number = randint(0, perimeter - 1)

        if tile_number < width:
            x, y = tile_number, 0
        elif tile_number < width + height - 1:
            x, y = width - 1, tile_number - width + 1
        elif tile_number < 2 * width + height - 3:
            x, y = 2 * width + height - 3 - tile_number, height - 1
        else:
            x, y = 0, perimeter - tile_number - 1

        return self.level.get_grid()[y][x]

    def on_arrive_ai(self) -> None:
        print(f'{self} has reach his Goal')

        return super().on_arrive_ai()

    def update_tracking(self) -> None:
        print('Generate New Tracking')

        if self._tracking_tile is None:
            return

        self.go_to(self._tracking_tile)
        super().update_tracking()
