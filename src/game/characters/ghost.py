from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.game.characters import Player

from src.core import Collider, Displayable, Entity, Level, Tile, Edible
from src.graphics import ImageTexture, OperationEnum, Position
from src.utils import Pos
from src.game.characters.player_state import PlayerState


class Ghost(Edible, Collider, Displayable, Entity):
    def __init__(self, name: str, tile: Pos | Tile, level: 'Level') -> None:
        super().__init__(
            name=id,
            tile=tile,
            level=level,
            solid=True,
            proportion=0.9,
            edible=False,
            reward=100
        )

    def on_collision(self, other: 'Collider') -> None:
        if not isinstance(other, Entity):
            return

        super().on_collision(other)

    def on_collision_exit(self, other: 'Collider') -> None:
        super().on_collision_exit(other)

    def init_mesh(self) -> None:
        self._mesh = ImageTexture(
            path='assets/characters/ghosts/red/east_0.png',
            position=Position(0, 0),
            width=0,
            height=0,
            operation=OperationEnum.SET,
            is_dynamic=False,
        )

    def eat(self, eater: 'Player') -> bool:
        if eater.get_state() == PlayerState.SUPER:
            self.set_edible(True)

        return_state: bool = super().eat(eater)

        self.set_edible(False)

        return return_state

    def update(self, dt: float) -> None:
        pass
