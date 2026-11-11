from src.app import App
from src.core import Entity, Level, Tile
from src.game.characters.ghost_type import GhostType
from src.graphics import Color
from src.texture.texture_keys import TextureKeys
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
                reward: float,
                app: App
            ) -> None:
        """
        Initialize the instance.

        Args:
            id: Identifier assigned to the object.
            tile: Grid tile occupied by or assigned to the entity.
            level: Level containing the entity or navigation data.
            reward: Reward used by the operation.
            app: Application instance that owns the object.
        """
        self._texture_path = 'assets/characters/ghosts/red'
        self._tracking_entity = level._entities.get(Player)

        super().__init__(
            name=f'blinky_ghost_{id}',
            tile=tile,
            level=level,
            update_tracking_interval=-1,
            reward=reward,
            path_color=Color(127, 0, 0, 100),
            app=app,
            ghost_type=GhostType.Blinky,
            texture_key=TextureKeys.GHOST_BLINKY
        )

    def get_chase_tracking_tile(self) -> Tile:
        """
        Return the current chase tracking tile.

        Returns:
            The current chase tracking tile.
        """
        return self._tracking_entity.get_tile()

    def on_arrive_ai(self) -> None:
        """
        Handle the arrive ai event.
        """
        return super().on_arrive_ai()
