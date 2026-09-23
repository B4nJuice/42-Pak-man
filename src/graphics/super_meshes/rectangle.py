from src.graphics import Position, OperationEnum, Color, SuperMesh, MeshLayer
from src.graphics.meshes import Polygon


class Rectangle(SuperMesh):
    def __init__(
                self,
                color: Color,
                position: Position,
                width: int,
                height: int,
                thickness: int,
                operation: OperationEnum = OperationEnum.SET,
                is_dynamic: bool = False,
                smooth_end: bool = False
            ) -> None:
        super().__init__(
            color,
            operation=operation,
            is_dynamic=is_dynamic
        )

        self.position: Position = position
        self.width: int = width
        self.height: int = height
        self.thickness: int = thickness
        self.smooth_end: bool = smooth_end

        self.layer: MeshLayer = MeshLayer()

        self.init()

    def init(self) -> None:
        self.position2: Position = Position(
            self.position.x + self.width, self.position.y
        )
        self.position3: Position = Position(
                self.position.x + self.width, self.position.y + self.height
            )
        self.position4: Position = Position(
                self.position.x, self.position.y + self.height
            )

        self.rectangle: Polygon = Polygon(
                self.color,
                [
                    self.position,
                    self.position2,
                    self.position3,
                    self.position4,
                ],
                operation=self.operation,
                thickness=self.thickness,
                is_dynamic=self.is_dynamic,
                smooth_end=self.smooth_end
            )

        self.layer.meshes.append(self.rectangle)

    def refresh(self) -> None:
        self.position2.x = self.position.x + self.width
        self.position2.y = self.position.y

        self.position3.x = self.position.x + self.width
        self.position3.y = self.position.y + self.height

        self.position4.x = self.position.x
        self.position4.y = self.position.y + self.height

        self.rectangle.operation = self.operation
        self.rectangle.color = self.color
        self.rectangle.thickness = self.thickness

    def get_layer(self) -> MeshLayer:
        return self.layer

    def set_position(self, position: Position) -> None:
        self.position.x = position.x
        self.position.y = position.y
        self.refresh()

    def set_width(self, width: int) -> None:
        self.width = width
        self.refresh()

    def set_height(self, height: int) -> None:
        self.height = height
        self.refresh()

    def set_thickness(self, thickness: int) -> None:
        self.thickness = thickness
        self.refresh

    def set_operation(self, operation: OperationEnum) -> None:
        self.operation = operation
        self.refresh()

    def set_color(self, color: Color) -> None:
        self.color = color
        self.refresh()
