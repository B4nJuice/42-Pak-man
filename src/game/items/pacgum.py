from src.core import Collider, Displayable, Entity, Level, Tile
from src.graphics import Color, OperationEnum, Plane, Position
from src.utils import Pos


class PacGum(Collider, Displayable, Entity):
    def __init__(self, id: str, pos: Pos | Tile, level: Level) -> None:
        super().__init__(
            name=id,
            tile=pos,
            level=level,
            solid=False,
            radius=0.1,
        )

        self.init_mesh()

    def init_mesh(self) -> None:
        self._mesh = Plane(
            color=Color(255, 255, 255),
            positions=(Position(40, 3), Position(45, 7)),
            operation=OperationEnum.SET,
            is_dynamic=True,
        )

    def update_mesh(self) -> None:
        pass

    def on_collision(self, other: 'Collider') -> None:
        if not isinstance(other, Entity):
            return

        print(f'Pacgum {self.get_name()!r} collided with {other.get_name()!r}')
        return super().on_collision(other)
