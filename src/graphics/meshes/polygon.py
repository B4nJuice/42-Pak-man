from ..color import Color, OperationEnum
from ..mesh import Mesh
from ..position import Position


class Polygon(Mesh):
    positions: list[Position]
    thickness: int
    smooth_end: bool

    def __init__(
                self,
                color: Color,
                positions: list[Position],
                operation: OperationEnum = OperationEnum.SET,
                thickness: int = 1,
                dynamic: bool = False,
                smooth_end: bool = False
            ) -> None:
        super().__init__(
                color,
                operation,
                dynamic
            )

        self.positions = positions
        self.thickness = thickness
        self.smooth_end = smooth_end
