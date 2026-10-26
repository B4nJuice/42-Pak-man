from collections.abc import Callable
from enum import Enum

from src.graphics.color import Color, OperationEnum
from src.graphics.mesh_layer import MeshLayer
from src.graphics.meshes import Plane
from src.graphics.position import Position
from src.graphics.super_mesh import SuperMesh


class ButtonState(Enum):
    NORMAL = "normal"
    HOVER = "hover"
    SELECTED = "selected"


class Button(SuperMesh):
    position: Position
    width: int
    height: int
    normal_color: Color
    hover_color: Color
    selected_color: Color
    state: ButtonState
    hovered: bool
    selected: bool
    layer: MeshLayer
    plane: Plane

    def __init__(
                self,
                position: Position,
                width: int,
                height: int,
                normal_color: Color,
                hover_color: Color,
                selected_color: Color | None = None,
                state: ButtonState = ButtonState.NORMAL,
                operation: OperationEnum = OperationEnum.ALPHA,
                dynamic: bool = False,
                on_click: Callable | None = None,
            ) -> None:
        super().__init__(
            normal_color,
            operation=operation,
            dynamic=dynamic,
        )

        self.position = position
        self.width = width
        self.height = height
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.selected_color = selected_color or hover_color
        self.state = ButtonState.NORMAL
        self.hovered = False
        self.selected = False
        self.layer = MeshLayer()

        self.plane = Plane(
            self.get_color(),
            (
                self.position,
                Position(
                    self.position.x + self.width,
                    self.position.y + self.height,
                ),
            ),
            operation=self.get_operation(),
            dynamic=self.is_dynamic(),
            on_click=on_click,
        )
        self.layer.meshes.append(self.plane)

        self.set_state(state)

    def _current_color(self) -> Color:
        if self.selected:
            return self.selected_color
        if self.hovered:
            return self.hover_color
        return self.normal_color

    def _sync_state(self) -> None:
        if self.selected:
            self.state = ButtonState.SELECTED
        elif self.hovered:
            self.state = ButtonState.HOVER
        else:
            self.state = ButtonState.NORMAL

    def get_layer(self) -> MeshLayer:
        return self.layer

    def refresh(self) -> None:
        self.plane.positions[1].x = self.position.x + self.width
        self.plane.positions[1].y = self.position.y + self.height
        self.plane.set_color(self._current_color())
        self.plane.set_operation(self.get_operation())

    def set_state(self, state: ButtonState) -> None:
        self.state = state
        self.hovered = state is ButtonState.HOVER
        self.selected = state is ButtonState.SELECTED
        self.set_color(self._current_color())
        self.refresh()

    def set_selected(self, selected: bool) -> None:
        self.selected = selected
        self._sync_state()
        self.refresh()

    def set_hovered(self, hovered: bool) -> None:
        self.hovered = hovered
        self._sync_state()
        self.refresh()

    def set_position(self, position: Position) -> None:
        self.position = position
        self.refresh()

    def set_size(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.refresh()

    def set_normal_color(self, color: Color) -> None:
        self.normal_color = color
        self.refresh()

    def set_hover_color(self, color: Color) -> None:
        self.hover_color = color
        self.refresh()

    def set_selected_color(self, color: Color) -> None:
        self.selected_color = color
        self.refresh()

    def set_operation(self, operation: OperationEnum) -> None:
        super().set_operation(operation)
        self.plane.set_operation(operation)

    def set_color(self, color: Color) -> None:
        super().set_color(color)
        self.plane.set_color(color)
