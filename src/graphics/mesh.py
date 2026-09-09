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
        self.dirty: bool = True
        self.hidden: bool = False
        self.is_dynamic: bool = is_dynamic

        self.clean_pixel: list[list[int]] = []
        self.dirty_pixel: list[list[int]] = []
