from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from src.graphics.color import Color, OperationEnum
from src.graphics.font import Font
from src.graphics.mesh_layer import MeshLayer
from src.graphics.meshes import Plane
from src.graphics.position import Position
from src.graphics.super_mesh import SuperMesh
from src.graphics.super_meshes.font_sequence import AlignEnum, FontSequence
from src.graphics.super_meshes.rectangle import Rectangle


class ButtonState(Enum):
    NORMAL = "normal"
    HOVER = "hover"
    SELECTED = "selected"


@dataclass(frozen=True)
class ButtonStyle:
    color: Color
    border_color: Color | None = None
    border_thickness: int = 0


@dataclass(frozen=True)
class ButtonTheme:
    normal: ButtonStyle
    hover: ButtonStyle | None = None
    selected: ButtonStyle | None = None

    def get_for_state(self, state: ButtonState) -> ButtonStyle:
        """
        Return the current for state.

        Args:
            state: State used by the operation.

        Returns:
            The current for state.
        """
        if state is ButtonState.SELECTED and self.selected is not None:
            return self.selected
        if state is ButtonState.HOVER and self.hover is not None:
            return self.hover
        return self.normal


@dataclass
class ButtonTextConfig:
    text: str = ""
    font: Font | None = None
    color: Color | None = None
    alignment: AlignEnum = AlignEnum.CENTER
    offset_x: int = 0
    offset_y: int = 0
    scale: float = 1.0
    spacing: int = 0
    state_texts: dict[ButtonState, str] = field(default_factory=dict)
    state_colors: dict[ButtonState, Color] = field(default_factory=dict)
    visible_states: set[ButtonState] = field(
        default_factory=lambda: {
            ButtonState.NORMAL,
            ButtonState.HOVER,
            ButtonState.SELECTED,
        }
    )

    def get_text_for_state(self, state: ButtonState) -> str:
        """
        Return the current text for state.

        Args:
            state: State used by the operation.

        Returns:
            The current text for state.
        """
        return self.state_texts.get(state, self.text)

    def get_color_for_state(self, state: ButtonState) -> Color | None:
        """
        Return the current color for state.

        Args:
            state: State used by the operation.

        Returns:
            The current color for state.
        """
        return self.state_colors.get(state, self.color)

    def is_visible_for_state(self, state: ButtonState) -> bool:
        """
        Check whether the visible for state condition holds.

        Args:
            state: State used by the operation.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        return state in self.visible_states


class Button(SuperMesh):
    position: Position
    width: int
    height: int
    normal_color: Color
    hover_color: Color
    selected_color: Color
    border_thickness: int
    border_color: Color
    hover_border_color: Color
    selected_border_color: Color
    state: ButtonState
    hovered: bool
    selected: bool
    layer: MeshLayer
    plane: Plane
    border: Rectangle | None
    theme: ButtonTheme
    texts: list[ButtonTextConfig]
    _text_sequences: list[FontSequence]

    def __init__(
                self,
                position: Position,
                width: int,
                height: int,
                normal_color: Color,
                hover_color: Color | None = None,
                selected_color: Color | None = None,
                state: ButtonState = ButtonState.NORMAL,
                operation: OperationEnum = OperationEnum.ALPHA,
                on_click: Callable | None = None,
                on_hover: Callable | None = None,
                border_thickness: int = 0,
                border_color: Color | None = None,
                hover_border_color: Color | None = None,
                selected_border_color: Color | None = None,
                theme: ButtonTheme | None = None,
                texts: list[ButtonTextConfig] | None = None,
            ) -> None:
        """
        Initialize the instance.

        Args:
            position: Screen or world coordinates of the object.
            width: Width of the screen or rendered element.
            height: Height of the screen or rendered element.
            normal_color: Normal color used by the operation.
            hover_color: Hover color used by the operation.
            selected_color: Selected color used by the operation.
            state: State used by the operation.
            operation: Operation used by the operation.
            on_click: On click used by the operation.
            on_hover: On hover used by the operation.
            border_thickness: Border thickness used by the operation.
            border_color: Border color used by the operation.
            hover_border_color: Hover border color used by the operation.
            selected_border_color: Selected border color used by the operation.
            theme: Theme used by the operation.
            texts: Texts used by the operation.
        """
        super().__init__(
            normal_color,
            operation=operation,
        )

        self.position = position
        self.width = width
        self.height = height
        self.normal_color = normal_color
        self.hover_color = hover_color or normal_color
        self.selected_color = selected_color or self.hover_color
        self.border_thickness = max(0, border_thickness)
        self.border_color = border_color or normal_color
        self.hover_border_color = hover_border_color or self.hover_color
        self.selected_border_color = (
            selected_border_color or self.selected_color
        )
        self.state = ButtonState.NORMAL
        self.hovered = False
        self.selected = False
        self.layer = MeshLayer()
        self.theme = theme or ButtonTheme(
            normal=ButtonStyle(
                color=normal_color,
                border_color=self.border_color,
                border_thickness=self.border_thickness,
            ),
            hover=ButtonStyle(
                color=self.hover_color,
                border_color=self.hover_border_color,
                border_thickness=self.border_thickness,
            ),
            selected=ButtonStyle(
                color=self.selected_color,
                border_color=self.selected_border_color,
                border_thickness=self.border_thickness,
            ),
        )
        self.texts = texts or []
        self._text_sequences = []

        def _on_hover() -> Any:
            """
            Handle on hover.

            Returns:
                The value produced by the on hover operation.
            """
            if on_hover:
                return on_hover()

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
            on_click=on_click,
            on_hover=_on_hover,
        )
        self.layer.meshes.append(self.plane)

        self.border = None
        if self.border_thickness > 0:
            self.border = Rectangle(
                self._current_border_color(),
                self.position,
                self.width,
                self.height,
                self.border_thickness,
                operation=self.get_operation(),
                smooth_end=True
            )
            self.layer.meshes.append(self.border)

        for text_config in self.texts:
            self.add_text(text_config)

        self.set_state(state)

    def init(self) -> None:
        """
        Initialize the associated state.
        """
        pass

    def _current_style(self) -> ButtonStyle:
        """
        Handle current style.

        Returns:
            The value produced by the current style operation.
        """
        return self.theme.get_for_state(self.state)

    def _current_color(self) -> Color:
        """
        Handle current color.

        Returns:
            The value produced by the current color operation.
        """
        if self.selected:
            return self.selected_color
        if self.hovered:
            return self.hover_color
        return self.normal_color

    def _current_border_color(self) -> Color:
        """
        Handle current border color.

        Returns:
            The value produced by the current border color operation.
        """
        if self.selected:
            return self.selected_border_color
        if self.hovered:
            return self.hover_border_color
        return self.border_color

    def _sync_state(self) -> None:
        """
        Handle sync state.
        """
        if self.selected:
            self.state = ButtonState.SELECTED
        elif self.hovered:
            self.state = ButtonState.HOVER
        else:
            self.state = ButtonState.NORMAL

    def add_text(self, config: ButtonTextConfig) -> FontSequence:
        """
        Add the text to the collection.

        Args:
            config: Configuration values used to initialize the component.

        Returns:
            The value produced by the add text operation.
        """
        if config.font is None:
            raise ValueError(
                "ButtonTextConfig.font is required to render text"
            )

        label = FontSequence(
            config.get_text_for_state(self.state),
            config.font,
            config.get_color_for_state(self.state) or self._current_color(),
            Position(
                self.position.x + (self.width // 2) + config.offset_x,
                self.position.y + (self.height // 2) + config.offset_y,
            ),
            spacing=config.spacing,
            align=config.alignment,
            operation=self.get_operation(),
        )
        label.set_scale(config.scale)
        self._text_sequences.append(label)
        self.layer.meshes.append(label)
        return label

    def get_layer(self) -> MeshLayer:
        """
        Return the current layer.

        Returns:
            The current layer.
        """
        return self.layer

    def _refresh_texts(self) -> None:
        """
        Handle refresh texts.
        """
        for index, text_config in enumerate(self.texts):
            if index >= len(self._text_sequences):
                continue

            sequence = self._text_sequences[index]
            if not text_config.is_visible_for_state(self.state):
                sequence.layer.meshes.clear()
                continue

            sequence.position = Position(
                self.position.x + (self.width // 2) + text_config.offset_x,
                self.position.y + (self.height // 2) + text_config.offset_y,
            )
            sequence.set_sequence_text(
                text_config.get_text_for_state(self.state)
            )
            sequence.set_color(
                text_config.get_color_for_state(self.state)
                or self._current_color()
            )
            sequence.set_sequence_text(
                text_config.get_text_for_state(self.state)
            )
            sequence.set_operation(self.get_operation())
            sequence.align = text_config.alignment
            sequence.set_scale(text_config.scale)

    def refresh(self) -> None:
        """
        Refresh the rendered state.
        """
        self.plane.positions[1].x = self.position.x + self.width
        self.plane.positions[1].y = self.position.y + self.height
        self.plane.set_color(self._current_color())
        self.plane.set_operation(self.get_operation())

        if self.border is not None:
            self.border.position = self.position
            self.border.width = self.width
            self.border.height = self.height
            self.border.thickness = self.border_thickness
            self.border.set_color(self._current_border_color())
            self.border.set_operation(self.get_operation())
            self.border.refresh()

        self._refresh_texts()

    def set_state(self, state: ButtonState) -> None:
        """
        Assign the state.

        Args:
            state: State used by the operation.
        """
        self.state = state
        self.hovered = state is ButtonState.HOVER
        self.selected = state is ButtonState.SELECTED
        self.set_color(self._current_color())
        self.refresh()

    def set_selected(self, selected: bool) -> None:
        """
        Assign the selected.

        Args:
            selected: Selected used by the operation.
        """
        self.selected = selected
        self._sync_state()
        self.refresh()

    def set_hovered(self, hovered: bool) -> None:
        """
        Assign the hovered.

        Args:
            hovered: Hovered used by the operation.
        """
        self.hovered = hovered
        self._sync_state()
        self.refresh()

    def set_position(self, position: Position) -> None:
        """
        Assign the position.

        Args:
            position: Screen or world coordinates of the object.
        """
        self.position = position
        self.refresh()

    def set_size(self, width: int, height: int) -> None:
        """
        Assign the size.

        Args:
            width: Width of the screen or rendered element.
            height: Height of the screen or rendered element.
        """
        self.width = width
        self.height = height
        self.refresh()

    def set_normal_color(self, color: Color) -> None:
        """
        Assign the normal color.

        Args:
            color: Color applied to the rendered element.
        """
        self.normal_color = color
        self.refresh()

    def set_hover_color(self, color: Color) -> None:
        """
        Assign the hover color.

        Args:
            color: Color applied to the rendered element.
        """
        self.hover_color = color
        self.refresh()

    def set_selected_color(self, color: Color) -> None:
        """
        Assign the selected color.

        Args:
            color: Color applied to the rendered element.
        """
        self.selected_color = color
        self.refresh()

    def set_border_thickness(self, thickness: int) -> None:
        """
        Assign the border thickness.

        Args:
            thickness: Thickness used by the operation.
        """
        self.border_thickness = max(0, thickness)
        if self.border is None and self.border_thickness > 0:
            self.border = Rectangle(
                self._current_border_color(),
                self.position,
                self.width,
                self.height,
                self.border_thickness,
                operation=self.get_operation(),
            )
            self.layer.meshes.append(self.border)
        elif self.border is not None and self.border_thickness <= 0:
            self.layer.meshes.remove(self.border)
            self.border = None
        self.refresh()

    def set_border_color(self, color: Color) -> None:
        """
        Assign the border color.

        Args:
            color: Color applied to the rendered element.
        """
        self.border_color = color
        self.refresh()

    def set_hover_border_color(self, color: Color) -> None:
        """
        Assign the hover border color.

        Args:
            color: Color applied to the rendered element.
        """
        self.hover_border_color = color
        self.refresh()

    def set_selected_border_color(self, color: Color) -> None:
        """
        Assign the selected border color.

        Args:
            color: Color applied to the rendered element.
        """
        self.selected_border_color = color
        self.refresh()

    def set_theme(self, theme: ButtonTheme) -> None:
        """
        Assign the theme.

        Args:
            theme: Theme used by the operation.
        """
        self.theme = theme
        self.refresh()

    def set_operation(self, operation: OperationEnum) -> None:
        """
        Assign the operation.

        Args:
            operation: Operation used by the operation.
        """
        super().set_operation(operation)
        self.plane.set_operation(operation)
        if self.border is not None:
            self.border.set_operation(operation)
        for sequence in self._text_sequences:
            sequence.set_operation(operation)

    def set_color(self, color: Color) -> None:
        """
        Assign the color.

        Args:
            color: Color applied to the rendered element.
        """
        super().set_color(color)
        self.plane.set_color(color)

    def sim_click(self, *args: Any, **kwargs: Any) -> Any:
        """
        Handle sim click.

        Args:
            args: Command-line arguments passed to the application.
            kwargs: Kwargs used by the operation.

        Returns:
            The value produced by the sim click operation.
        """
        return self.plane.sim_click(*args, **kwargs)
