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
        self._tracking_entity = level.entities.get(Player)[0]
        if not self._tracking_entity:
            raise ValueError('Error can not reach player')

        super().__init__(
            name=f'red_ghost_{id}',
            tile=tile,
            level=level,
            update_tracking_interval=None
        )

    def go_to(self, tile: Tile) -> None:
        path = self.a_star.find_path(
            start=self.get_target_tile(),
            end=tile
        )

        self.clear_next_moves()
        self.apply_path(path)

    def update(self, dt: float) -> None:
        self.set_tracking_tile(self._tracking_entity.get_tile())

        return super().update(dt)

    def update_tracking(self) -> None:
        print('Generate New Tracking')

        if self._tracking_tile is None:
            return

        self.go_to(self._tracking_tile)
        super().update_tracking()
