from src.core import Collider, Displayable, Entity, Level, Tile, Edible
from src.graphics import ImageTexture, OperationEnum, Position
from src.utils import Pos


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

    def update(self, dt: float) -> None:
        pass
