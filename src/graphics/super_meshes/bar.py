from src.graphics.color import Color, OperationEnum
from src.graphics.mesh_layer import MeshLayer
from src.graphics.meshes import Plane
from src.graphics.position import Position
from src.graphics.super_mesh import SuperMesh
from src.graphics.super_meshes.rectangle import Rectangle


class Bar(SuperMesh):
    def __init__(
                self,
                color: Color,
                border_color: Color,
                position: Position,
                width: int,
                height: int,
                border_thickness: int,
                goal: float,
                progression: float = 0,
                operation: OperationEnum = OperationEnum.SET,
                dynamic: bool = False,
                smooth_end: bool = False,
            ) -> None:
        super().__init__(
            color,
            operation=operation,
            dynamic=dynamic
        )

        self.width: int = width
        self.height: int = height
        self.border_thickness: int = border_thickness
        self.border_color: Color = border_color
        self.smooth_end: bool = smooth_end
        self.position = position
        self.goal: float = goal
        self.progression: float = progression

        self.layer: MeshLayer = MeshLayer()

        self.init()

    def init(self) -> None:
        percentage: float = self._percentage()

        self.inner: Plane = Plane(
            self.get_color(),
            (
                self.position, Position(
                        int(self.position.x + self.width * percentage),
                        self.position.y + self.height,
                )
            ),
            operation=self.get_operation(),
            dynamic=self.is_dynamic()
        )

        self.layer.meshes.append(self.inner)

        self.border: Rectangle = Rectangle(
            self.border_color,
            self.position,
            self.width,
            self.height,
            self.border_thickness,
            operation=self.get_operation(),
            dynamic=self.is_dynamic(),
            smooth_end=self.smooth_end
        )

        self.layer.meshes.append(self.border)

    def _percentage(self) -> float:
        if self.goal <= 0:
            return 0.0
        return min(1, self.progression / self.goal)

    def refresh(self) -> None:
        percentage = self._percentage()
        self.inner.positions[1].x = self.position.x + round(self.width * percentage)
        self.inner.positions[1].y = self.position.y + self.height
        self.inner.set_color(self.get_color())
        self.inner.set_operation(self.get_operation())

        self.border.position = self.position
        self.border.width = self.width
        self.border.height = self.height
        self.border.thickness = self.border_thickness
        self.border.set_color(self.border_color)
        self.border.set_operation(self.get_operation())
        self.border.refresh()

    def get_layer(self) -> MeshLayer:
        return self.layer

    def set_progression(self, progression: float) -> None:
        self.progression = max(0, progression)
        self.refresh()

    def set_goal(self, goal: float) -> None:
        self.goal = max(0, goal)
        self.refresh()

    def set_color(self, color: Color) -> None:
        super().set_color(color)
        self.refresh()

    def set_border_color(self, color: Color) -> None:
        self.border_color = color
        self.refresh()
