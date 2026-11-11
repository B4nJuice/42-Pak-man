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
                smooth_end: bool = False
            ) -> None:
        """
        Initialize the instance.

        Args:
            color: Color applied to the rendered element.
            positions: Positions used by the operation.
            operation: Operation used by the operation.
            thickness: Thickness used by the operation.
            smooth_end: Smooth end used by the operation.
        """
        super().__init__(
                color,
                operation,
            )

        self.positions = positions
        self.thickness = thickness
        self.smooth_end = smooth_end
