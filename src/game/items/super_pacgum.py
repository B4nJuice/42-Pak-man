from src.core import Collider, Displayable, Entity, Level, Tile
from src.graphics import ImageTexture, OperationEnum, Position
from src.utils import Pos


class SuperPacGum(Collider, Displayable, Entity):
    def __init__(self, id: str, pos: Pos | Tile, level: Level) -> None:
        super().__init__(
            name=id,
            tile=pos,
            level=level,
            solid=False,
            radius=0.15,
            proportion=0.3
        )

        self.init_mesh()

    def init_mesh(self) -> None:
        self._mesh = ImageTexture(
            path='assets/items/super_pacgum.png',
            position=Position(0, 0),
            width=0,
            height=0,
            operation=OperationEnum.SET,
            is_dynamic=False,
        )

    def update_mesh(self) -> None:
        pass

    def on_collision(self, other: 'Collider') -> None:
        if not isinstance(other, Entity):
            return

        return super().on_collision(other)
