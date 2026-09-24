from src.graphics import Position, OperationEnum, Color, SuperMesh, MeshLayer
from src.graphics.super_meshes import Rectangle
from src.graphics.meshes import Plane

class Bar(SuperMesh):
    def __init__(
                self,
                color: Color,
                border_color: Color,
                position: Position,
                width: int,
                height: int,
                border_thickness: int,
                goal: int,
                progression: int = 0,
                operation: OperationEnum = OperationEnum.SET,
                is_dynamic: bool = False,
                smooth_end: bool = False,
            ) -> None:
        super().__init__(
            color,
            operation=operation,
            is_dynamic=is_dynamic
        )

        self.width: int = width
        self.height: int = height
        self.border_thickness: int = border_thickness
        self.border_color: Color = border_color
        self.smooth_end: bool = smooth_end
        self.position = position
        self.goal: int = goal
        self.progression: int = progression

        self.layer: MeshLayer = MeshLayer()

        self.init()

    def init(self) -> None:
        percentage: float = self._percentage()

        self.inner: Plane = Plane(
            self.color,
            (
                self.position, Position(
                        self.position.x + self.width * percentage,
                        self.position.y + self.height * percentage,
                )
            ),
            operation=self.operation,
            is_dynamic=self.is_dynamic
        )

        self.layer.meshes.append(self.inner)

        self.border: Rectangle = Rectangle(
            self.border_color,
            self.position,
            self.width,
            self.height,
            self.border_thickness,
            operation=self.operation,
            is_dynamic=self.is_dynamic,
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
        self.inner.color = self.color
        self.inner.operation = self.operation

        self.border.position = self.position
        self.border.width = self.width
        self.border.height = self.height
        self.border.thickness = self.border_thickness
        self.border.color = self.border_color
        self.border.operation = self.operation
        self.border.refresh()

    def get_layer(self) -> MeshLayer:
        return self.layer

    def set_progression(self, progression: int) -> None:
        self.progression = max(0, progression)
        self.refresh()

    def set_goal(self, goal: int) -> None:
        self.goal = max(0, goal)
        self.refresh()

    def set_color(self, color: Color) -> None:
        self.color = color
        self.refresh()

    def set_border_color(self, color: Color) -> None:
        self.border_color = color
        self.refresh()
