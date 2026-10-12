from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.tile import Tile
    from .direction import Direction


Vec2 = tuple[float, float]
Pos = tuple[int, int]
Path = list[tuple['Tile', 'Direction']]
