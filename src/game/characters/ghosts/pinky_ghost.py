from src.core import Entity, Level, Tile
from src.utils import Direction, Pos

from ..ghost import Ghost
from ..player import Player


class PinkyGhost(Ghost):
    _tracking_entity: Entity

    def __init__(self, id: int, tile: Pos | Tile, level: Level) -> None:
        self._texture_path = 'assets/characters/ghosts/pink'
        self._tracking_entity = level.entities.get(Player)

        super().__init__(
            name=f'pinky_ghost_{id}',
            tile=tile,
            level=level,
            update_tracking_interval=0
        )

    def get_tracking_tile(self) -> Tile:
        my_direction: Direction | None = self.get_direction()
        player_tile: Tile = self._tracking_entity.get_tile()

        if my_direction is None:
             return player_tile
        return self.level.get_tile_ahead(player_tile, my_direction, 4)

    def on_arrive_ai(self) -> None:
        print(f'{self} has reach his Goal')

        return super().on_arrive_ai()

    def update_tracking(self) -> None:
        print('Generate New Tracking')

        if self._tracking_tile is None:
            return

        self.go_to(self._tracking_tile)
        super().update_tracking()
