from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.tile import Tile  # noqa: F401
    from .direction import Direction  # noqa: F401


Vec2 = tuple[float, float]
Pos = tuple[int, int]
Path = list[tuple['Tile', 'Direction']]
