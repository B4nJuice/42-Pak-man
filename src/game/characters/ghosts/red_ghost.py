from src.core import AStar, Entity, Level, Tile
from src.utils import Pos

from ..ghost import Ghost
from ..player import Player


class RedGhost(Ghost):
    a_star: AStar
    _tracking_entity: Entity

    def __init__(self, id: int, tile: Pos | Tile, level: Level) -> None:
        self._texture_path = 'assets/characters/ghosts/red'
        self.a_star = AStar(level)
        self._tracking_entity = level.entities.get(Player)

        super().__init__(
            name=f'red_ghost_{id}',
            tile=tile,
            level=level,
            update_tracking_interval=None
        )

    def get_tracking_tile(self) -> Tile:
        return self._tracking_entity.get_tile()

    def update_tracking(self) -> None:
        print('Generate New Tracking')

        if self._tracking_tile is None:
            return

        self.go_to(self._tracking_tile)
        super().update_tracking()
