from pathlib import Path

from src.core import AI, Collider, Displayable, Entity, Level, Tile
from src.core.movable import Movable
from src.graphics import ImageTexture
from src.utils import Direction, Pos


class Ghost(Collider, AI, Movable, Displayable, Entity):
    _texture_path: str
    _meshs: dict[Direction, list[ImageTexture]]
    _elapsed_time_traking_update: float
    _invalid_tracinkg_time: float | None
    _last_tile_tracking: Tile | None
    _force_update_tracking: bool

    def __init__(self, name: str, tile: Pos | Tile, level: Level) -> None:
        super().__init__(
            name=name,
            tile=tile,
            level=level,
            solid=True,
            proportion=0.9,
        )

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

    def init_tracking(self, update_interval: float | None) -> None:
        self._elapsed_time_traking_update = float('inf')
        self._invalid_tracinkg_time = update_interval
        self._last_tile_tracking = None
        self._force_update_tracking = False

    def update(self, dt: float) -> None:
        super().update(dt)

    def get_mesh(self) -> ImageTexture:
        if not self._direction:
            return self._meshs[Direction.EAST][0]

        return self._meshs[self._direction][0]

    def update_tracking(self) -> None:
        self._elapsed_time_traking_update = 0

    def force_update_tracking(self) -> None:
        self._force_update_tracking = True

    def need_to_update(self, dt: float, tile: Tile) -> bool:
        self._elapsed_time_traking_update += dt

        if self._force_update_tracking:
            self._force_update_tracking = False
            return True

        return self._last_tile_tracking != tile and \
        (
            self._invalid_tracinkg_time is not None and
            self._elapsed_time_traking_update >= self._invalid_tracinkg_time\
        )
