from src.core import Level, Tile
from src.utils import Direction, Pos

from ..ghost import Ghost
from ..player import Player


class PinkyGhost(Ghost):
    _tracking_entity: Player

    def __init__(
                self,
                id: int,
                tile: Pos | Tile,
                level: Level,
                reward: float
            ) -> None:
        self._texture_path = 'assets/characters/ghosts/pink'
        self._tracking_entity = level._entities.get(Player)

        super().__init__(
            name=f'pinky_ghost_{id}',
            tile=tile,
            level=level,
            update_tracking_interval=0,
            reward=reward
        )

    def get_tracking_tile(self) -> Tile:
        player_direction: Direction | None =\
                self._tracking_entity.get_direction()
        player_tile: Tile = self._tracking_entity.get_tile()

        if player_direction is None:
            return player_tile
        return self.level.get_tile_ahead(player_tile, player_direction, 4)

    def on_arrive_ai(self) -> None:
        return super().on_arrive_ai()

    def update_tracking(self) -> None:
        if self._tracking_tile is None:
            return

        self.go_to(self._tracking_tile)
        super().update_tracking()
