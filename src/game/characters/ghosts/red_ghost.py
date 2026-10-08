from src.core import AStar, Entity, Level, Tile

# from src.utils import Direction
from ..ghost import Ghost
from ..player import Player


class RedGhost(Ghost):
    a_star: AStar
    _tracking_entity: Entity

    def __init__(self, id: int, level: Level) -> None:
        self._texture_path = 'assets/characters/ghosts/red'
        self.a_star = AStar(level)
        self._tracking_entity = level.entities.get(Player)[0]
        if not self._tracking_entity:
            raise ValueError('Error can not reach player')

        self.init_tracking(0.2)
        super().__init__(f'red_ghost_{id}', (0, 0), level)

    def go_to(self, tile: Tile) -> None:
        path = self.a_star.find_path(
            start=self.get_target_tile(),
            end=tile
        )

        self.clear_next_moves()
        for _, direction in path:
            self.add_next_move(direction)

    def update(self, dt: float) -> None:
        if self.need_to_update(dt, self._tracking_entity.get_tile()):
            self.update_tracking()
        return super().update(dt)

    def update_tracking(self) -> None:
        print('Generate New Tracking')
        tile: Tile = self._tracking_entity.get_tile()
        self._last_tile_tracking = tile
        self.go_to(tile)

        super().update_tracking()
