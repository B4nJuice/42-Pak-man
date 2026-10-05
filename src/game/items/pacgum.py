from src.core import Collider, Displayable, Entity, Level, Tile
from src.graphics import ImageTexture
from src.utils import Pos


class PacGum(Collider, Displayable, Entity):
    def __init__(self, id: str, pos: Pos | Tile, level: Level) -> None:
        super().__init__(
            name=id,
            tile=pos,
            level=level,
            solid=False,
            radius=0.1,
            proportion=0.2
        )

        self.init_mesh()

    def init_mesh(self) -> None:
        self._mesh = ImageTexture.create_blank(
            'assets/items/pacgum.png',
        )

    def update_mesh(self) -> None:
        pass

    def on_collision(self, other: 'Collider') -> None:
        if not isinstance(other, Entity):
            return

        print(f'Pacgum {self.get_name()!r} collided with {other.get_name()!r}')
        return super().on_collision(other)
