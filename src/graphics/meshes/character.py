from typing import Any

from src.graphics import Mesh, Position, Color, OperationEnum

class Character(Mesh):
    def __init__(
                self,
                character: str,
                infos: dict[str, Any],
                color: Color,
                position: Position,
                operation: OperationEnum = OperationEnum.SET,
                is_dynamic: bool = False
            ) -> None:
        super().__init__(
                color,
                operation,
                is_dynamic
            )

        self.position: Position = position
        self.character: str = character
        self.infos: dict[str, Any] = infos
