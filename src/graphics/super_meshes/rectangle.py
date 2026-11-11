from src.graphics import Color, OperationEnum, Position
from src.graphics.mesh_layer import MeshLayer
from src.graphics.meshes import Polygon
from src.graphics.super_mesh import SuperMesh


class Rectangle(SuperMesh):
    position: Position
    width: int
    height: int
    thickness: int
    smooth_end: bool
    layer: MeshLayer
    position2: Position
    position3: Position
    position4: Position
    rectangle: Polygon

    def __init__(
                self,
                color: Color,
                position: Position,
                width: int,
                height: int,
                thickness: int,
                operation: OperationEnum = OperationEnum.SET,
                smooth_end: bool = False
            ) -> None:
        """
        Initialize the instance.

        Args:
            color: Color applied to the rendered element.
            position: Screen or world coordinates of the object.
            width: Width of the screen or rendered element.
            height: Height of the screen or rendered element.
            thickness: Thickness used by the operation.
            operation: Operation used by the operation.
            smooth_end: Smooth end used by the operation.
        """
        super().__init__(
            color,
            operation=operation,
        )

        self.position = position
        self.width = width
        self.height = height
        self.thickness = thickness
        self.smooth_end = smooth_end

        self.layer = MeshLayer()

        self.init()

    def init(self) -> None:
        """
        Initialize the associated state.
        """
        self.position2 = Position(
            self.position.x + self.width, self.position.y
        )
        self.position3 = Position(
                self.position.x + self.width, self.position.y + self.height
            )
        self.position4 = Position(
                self.position.x, self.position.y + self.height
            )

        self.rectangle = Polygon(
                self.get_color(),
                [
                    self.position,
                    self.position2,
                    self.position3,
                    self.position4,
                ],
                operation=self.get_operation(),
                thickness=self.thickness,
                smooth_end=self.smooth_end
            )

        self.layer.meshes.append(self.rectangle)

    def refresh(self) -> None:
        """
        Refresh the rendered state.
        """
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
        """
        Return the current layer.

        Returns:
            The current layer.
        """
        return self.layer

    def set_position(self, position: Position) -> None:
        """
        Assign the position.

        Args:
            position: Screen or world coordinates of the object.
        """
        self.position.x = position.x
        self.position.y = position.y
        self.refresh()

    def set_width(self, width: int) -> None:
        """
        Assign the width.

        Args:
            width: Width of the screen or rendered element.
        """
        self.width = width
        self.refresh()

    def set_height(self, height: int) -> None:
        """
        Assign the height.

        Args:
            height: Height of the screen or rendered element.
        """
        self.height = height
        self.refresh()

    def set_thickness(self, thickness: int) -> None:
        """
        Assign the thickness.

        Args:
            thickness: Thickness used by the operation.
        """
        self.thickness = thickness
        self.refresh()

    def set_operation(self, operation: OperationEnum) -> None:
        """
        Assign the operation.

        Args:
            operation: Operation used by the operation.
        """
        super().set_operation(operation)
        self.refresh()

    def set_color(self, color: Color) -> None:
        """
        Assign the color.

        Args:
            color: Color applied to the rendered element.
        """
        super().set_color(color)
        self.refresh()
