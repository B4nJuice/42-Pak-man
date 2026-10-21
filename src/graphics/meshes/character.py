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
                dynamic: bool = False
            ) -> None:
        super().__init__(
                color,
                operation,
                dynamic
            )

        self.position = position
        self.character = character
        self.infos = infos
        self.scale = 1.0

    def set_scale(self, scale: float) -> None:
        self.scale = scale
