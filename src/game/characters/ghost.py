from pathlib import Path

from src.core import AI, AStar, Collider, Displayable, Entity, Level, Tile
from src.core.movable import Movable
from src.graphics import ImageTexture
from src.utils import Direction, Pos


class Ghost(Collider, AI, Movable, Displayable, Entity):
    a_star: AStar
    _texture_path: str
    _meshs: dict[Direction, list[ImageTexture]]

    def __init__(self, name: str, tile: Pos | Tile, level: Level, update_tracking_interval: float | None = 0.6) -> None:
        super().__init__(
            name=name,
            tile=tile,
            level=level,
            solid=True,
            proportion=0.9,
            update_tracking_interval=update_tracking_interval
        )

        self.a_star = AStar(level)

    def init_mesh(self) -> None:
        self._meshs = {
            direction: [
                ImageTexture.create_blank(Path(
                    self._texture_path, f'{direction.to_string()}_{i}.png'
                ).as_posix())
                for i in range(1)
            ]
            for direction in Direction
        }

        self._mesh = self._meshs[Direction.EAST][0]


    def go_to(self, tile: Tile) -> None:
        path = self.a_star.find_path(
            start=self.get_target_tile(),
            end=tile
        )

        self.clear_next_moves()
        self.apply_path(path)

    def update(self, dt: float) -> None:
        self.update_ai(dt)
        self.update_mesh()

        super().update(dt)

    def get_mesh(self) -> ImageTexture:
        if not self._direction:
            return self._meshs[Direction.EAST][0]

        return self._meshs[self._direction][0]

    def get_texture(self) -> ImageTexture:
        if self._direction is None:
            return self._meshs[Direction.EAST][0]

        return self._meshs[self._direction][0]
