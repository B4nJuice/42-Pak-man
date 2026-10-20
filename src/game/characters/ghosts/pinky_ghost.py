from src.app import App
from src.core import Level, Tile
from src.game.characters.ghost_type import GhostType
from src.graphics import Color
from src.texture.texture_keys import TextureKeys
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
                reward: float,
                app: App
            ) -> None:
        self._texture_path = 'assets/characters/ghosts/pink'
        self._tracking_entity = level._entities.get(Player)

        super().__init__(
            name=f'pinky_ghost_{id}',
            tile=tile,
            level=level,
            update_tracking_interval=0,
            reward=reward,
            path_color=Color(127, 0, 110, 100),
            app=app,
            ghost_type=GhostType.Pinky,
            texture_key=TextureKeys.GHOST_PINKY
        )

    def get_chase_tracking_tile(self) -> Tile:
        player_direction: Direction | None =\
                self._tracking_entity.get_direction()
        player_tile: Tile = self._tracking_entity.get_tile()

        if player_direction is None:
            return player_tile
        return self.level.get_tile_ahead(player_tile, player_direction, 4)

    def on_arrive_ai(self) -> None:
        return super().on_arrive_ai()
