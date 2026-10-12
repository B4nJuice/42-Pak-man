from src.core import Entity, Level, Tile
from src.utils import Pos

from ..ghost import Ghost
from ..player import Player


class BlinkyGhost(Ghost):
    _tracking_entity: Entity

    def __init__(
                self,
                id: int,
                tile: Pos | Tile,
                level: Level,
                reward: float
            ) -> None:
        self._texture_path = 'assets/characters/ghosts/red'
        self._tracking_entity = level._entities.get(Player)

        super().__init__(
            name=f'blinky_ghost_{id}',
            tile=tile,
            level=level,
            update_tracking_interval=-1,
            reward=reward
        )

    def get_chase_tracking_tile(self) -> Tile:
        return self._tracking_entity.get_tile()

    def on_arrive_ai(self) -> None:
        return super().on_arrive_ai()

    def update_tracking(self) -> None:
        if self._tracking_tile is None:
            return

        self.go_to(self._tracking_tile)
        super().update_tracking()
