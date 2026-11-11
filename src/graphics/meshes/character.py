from typing import Any

from ..color import Color, OperationEnum
from ..mesh import Mesh
from ..position import Position


class Character(Mesh):
    position: Position
    character: str
    infos: dict[str, Any]
    scale: float

    def __init__(
                self,
                character: str,
                infos: dict[str, Any],
                color: Color,
                position: Position,
                operation: OperationEnum = OperationEnum.SET,
            ) -> None:
        """
        Initialize the instance.

        Args:
            character: Character used by the operation.
            infos: Infos used by the operation.
            color: Color applied to the rendered element.
            position: Screen or world coordinates of the object.
            operation: Operation used by the operation.
        """
        super().__init__(
                color,
                operation,
            )

        self.position = position
        self.character = character
        self.infos = infos
        self.scale = 1.0

    def set_scale(self, scale: float) -> None:
        """
        Assign the scale.

        Args:
            scale: Scale used by the operation.
        """
        self.scale = scale
