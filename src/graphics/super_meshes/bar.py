from src.graphics.color import Color, OperationEnum
from src.graphics.mesh_layer import MeshLayer
from src.graphics.meshes import Plane
from src.graphics.position import Position
from src.graphics.super_mesh import SuperMesh
from src.graphics.super_meshes.rectangle import Rectangle


class Bar(SuperMesh):
    width: int
    height: int
    border_thickness: int
    border_color: Color
    smooth_end: bool
    position: Position
    goal: float
    progression: float
    displayed_progression: float
    layer: MeshLayer
    inner: Plane
    border: Rectangle

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
                smooth_end: bool = False,
            ) -> None:
        """
        Initialize the instance.

        Args:
            color: Color applied to the rendered element.
            border_color: Border color used by the operation.
            position: Screen or world coordinates of the object.
            width: Width of the screen or rendered element.
            height: Height of the screen or rendered element.
            border_thickness: Border thickness used by the operation.
            goal: Goal used by the operation.
            progression: Progression used by the operation.
            operation: Operation used by the operation.
            smooth_end: Smooth end used by the operation.
        """
        super().__init__(
            color,
            operation=operation,
        )

        self.width = width
        self.height = height
        self.border_thickness = border_thickness
        self.border_color = border_color
        self.smooth_end = smooth_end
        self.position = position
        self.goal = goal
        self.progression = progression
        self.displayed_progression = progression

        self.layer = MeshLayer()

        self.init()

    def init(self) -> None:
        """
        Initialize the associated state.
        """
        percentage: float = self._percentage()

        self.inner = Plane(
            self.get_color(),
            (
                self.position, Position(
                        int(self.position.x + self.width * percentage),
                        self.position.y + self.height,
                )
            ),
            operation=self.get_operation(),
        )

        self.layer.meshes.append(self.inner)

        self.border = Rectangle(
            self.border_color,
            self.position,
            self.width,
            self.height,
            self.border_thickness,
            operation=self.get_operation(),
            smooth_end=self.smooth_end
        )

        self.layer.meshes.append(self.border)

    def _percentage(self) -> float:
        """
        Handle percentage.

        Returns:
            The value produced by the percentage operation.
        """
        if self.goal <= 0:
            return 0.0
        return min(1, self.progression / self.goal)

    def _displayed_percentage(self) -> float:
        """
        Handle displayed percentage.

        Returns:
            The value produced by the displayed percentage operation.
        """
        if self.goal <= 0:
            return 0.0
        return min(1, self.displayed_progression / self.goal)

    def refresh(self) -> None:
        """
        Refresh the rendered state.
        """
        percentage = self._displayed_percentage()
        self.inner.positions[1].x = self.position.x + round(
            self.width * percentage
        )
        self.inner.positions[1].y = self.position.y + self.height
        self.inner.set_color(self.get_color())
        self.inner.set_operation(self.get_operation())

    def refresh_border(self) -> None:
        """
        Handle refresh border.
        """
        self.border.position = self.position
        self.border.width = self.width
        self.border.height = self.height
        self.border.thickness = self.border_thickness
        self.border.set_color(self.border_color)
        self.border.set_operation(self.get_operation())
        self.border.refresh()

    def get_layer(self) -> MeshLayer:
        """
        Return the current layer.

        Returns:
            The current layer.
        """
        return self.layer

    def set_progression(self, progression: float) -> None:
        """
        Assign the progression.

        Args:
            progression: Progression used by the operation.
        """
        self.progression = max(0, progression)

        progression_diff: float = self.progression - self.displayed_progression

        if self.progression > self.displayed_progression:

            min_progression: float = min(
                self.goal * 0.02,
                progression_diff
            )

            self.displayed_progression += max((
                progression_diff
            ) * 0.09, min_progression)
        elif self.progression < self.displayed_progression:
            self.displayed_progression = 0

        self.refresh()

    def set_goal(self, goal: float) -> None:
        """
        Assign the goal.

        Args:
            goal: Goal used by the operation.
        """
        self.goal = max(0, goal)
        self.refresh()

    def set_color(self, color: Color) -> None:
        """
        Assign the color.

        Args:
            color: Color applied to the rendered element.
        """
        super().set_color(color)
        self.refresh()

    def set_border_color(self, color: Color) -> None:
        """
        Assign the border color.

        Args:
            color: Color applied to the rendered element.
        """
        self.border_color = color
        self.refresh()
