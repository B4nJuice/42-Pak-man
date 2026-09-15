from src.graphics import Position, OperationEnum, Color


class Mesh():
    def __init__(
                self,
                color: Color,
                operation: OperationEnum = OperationEnum.SET,
                is_dynamic: bool = False
            ) -> None:
        self.color: Color = color
        self.operation: OperationEnum = operation
        self.hidden: bool = False
        self.is_dynamic: bool = is_dynamic
