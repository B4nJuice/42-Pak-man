from src.core import Collider, Displayable, Entity, Level, Tile
from src.graphics import ImageTexture, OperationEnum, Position
from src.utils import Pos


class Ghost(Collider, Displayable, Entity):
    def __init__(self, name: str, tile: Pos | Tile, level: 'Level') -> None:
        super().__init__(
            name=id,
            tile=tile,
            level=level,
            solid=True,
            radius=0.45,
        )

    def on_collision(self, other: 'Collider') -> None:
        if not isinstance(other, Entity):
            return

        super().on_collision(other)

    def on_collision_exit(self, other: 'Collider') -> None:
        super().on_collision_exit(other)

    def init_mesh(self) -> None:
        self._mesh = ImageTexture(
            path='assets/characters/pacman/d0_0.png',
            position=Position(0, 0),
            width=0,
            height=0,
            operation=OperationEnum.SET,
            is_dynamic=False,
        )

    def update(self, dt: float) -> None:
        pass

    def update_mesh(self) -> None:
        return super().update_mesh()
