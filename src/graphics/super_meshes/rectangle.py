from src.graphics import Color, OperationEnum, Position
from src.graphics.mesh_layer import MeshLayer
from src.graphics.meshes import Polygon
from src.graphics.super_mesh import SuperMesh


class Rectangle(SuperMesh):
    def __init__(
                self,
                color: Color,
                position: Position,
                width: int,
                height: int,
                thickness: int,
                operation: OperationEnum = OperationEnum.SET,
                dynamic: bool = False,
                smooth_end: bool = False
            ) -> None:
        super().__init__(
            color,
            operation=operation,
            dynamic=dynamic
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
                self.get_color(),
                [
                    self.position,
                    self.position2,
                    self.position3,
                    self.position4,
                ],
                operation=self.get_operation(),
                thickness=self.thickness,
                dynamic=self.is_dynamic(),
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

        self.rectangle.set_operation(self.get_operation())
        self.rectangle.set_color(self.get_color())
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
        self.refresh()

    def set_operation(self, operation: OperationEnum) -> None:
        super().set_operation(operation)
        self.refresh()

    def set_color(self, color: Color) -> None:
        super().set_color(color)
        self.refresh()
