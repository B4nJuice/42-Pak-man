from src.app import App
from src.core import Level, Tile
from src.game.characters.ghost_type import GhostType
from src.graphics import Color
from src.texture.texture_keys import TextureKeys
from src.utils import Pos

from ..ghost import Ghost
from ..player import Player
from .blinky_ghost import BlinkyGhost


class InkyGhost(Ghost):
    _tracking_entity: Player
    _mirror_ghost: Ghost

    def __init__(
                self,
                id: int,
                tile: Pos | Tile,
                level: Level,
                reward: float,
                app: App
            ) -> None:
        self._texture_path = 'assets/characters/ghosts/cyan'
        self._tracking_entity = level._entities.get(Player)
        self._mirror_ghost = level._entities.get(BlinkyGhost)

        super().__init__(
            name=f'inky_ghost_{id}',
            tile=tile,
            level=level,
            update_tracking_interval=None,
            reward=reward,
            path_color=Color(0, 110, 127, 100),
            app=app,
            ghost_type=GhostType.Inky,
            texture_key=TextureKeys.GHOST_INKY
        )

    def get_chase_tracking_tile(self) -> Tile:
        player_tile: Tile = self._tracking_entity.get_tile()
        blinky_tile: Tile = self._mirror_ghost.get_tile()

        player_x, player_y = player_tile.get_pos()
        blinky_x, blinky_y = blinky_tile.get_pos()

        diff_x = player_x - blinky_x
        diff_y = player_y - blinky_y

        tracking_x: int = max(0, min(
                self.level.get_width() - 1, player_x + diff_x
            ))
        tracking_y: int = max(0, min(
                self.level.get_height() - 1, player_y + diff_y
            ))

        return self.level.get_grid()[tracking_y][tracking_x]

    def on_arrive_ai(self) -> None:
        return super().on_arrive_ai()
