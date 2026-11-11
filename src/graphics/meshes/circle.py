from ..color import Color, OperationEnum
from ..mesh import Mesh
from ..position import Position


class Circle(Mesh):
    position: Position
    radius: int
    thickness: int
    filled: bool

    def __init__(
                self,
                color: Color,
                position: Position,
                radius: int,
                operation: OperationEnum = OperationEnum.SET,
                thickness: int = 1,
                filled: bool = False,
            ) -> None:
        """
        Initialize the instance.

        Args:
            color: Color applied to the rendered element.
            position: Screen or world coordinates of the object.
            radius: Collision radius of the entity.
            operation: Operation used by the operation.
            thickness: Thickness used by the operation.
            filled: Filled used by the operation.
        """
        super().__init__(
                color,
                operation,
            )

        self.position = position
        self.radius = max(radius, 0)
        self.thickness = max(thickness, 0)
        self.filled = filled

    def get_position(self) -> Position:
        """
        Return the current position.

        Returns:
            The current position.
        """
        return self.position
