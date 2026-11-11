from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum

from src.graphics.color import Color, OperationEnum
from src.graphics.font import Font
from src.graphics.mesh_layer import MeshLayer
from src.graphics.meshes import Plane
from src.graphics.position import Position
from src.graphics.super_mesh import SuperMesh
from src.graphics.super_meshes.font_sequence import AlignEnum, FontSequence
from src.graphics.super_meshes.rectangle import Rectangle


class ToggleState(Enum):
    INACTIVE = "inactive"
    ACTIVE = "active"

    @classmethod
    def get(cls, value: bool) -> 'ToggleState':
        """
        Handle get.

        Args:
            value: Value to assign or apply.

        Returns:
            The value produced by the get operation.
        """
        if value:
            return cls.ACTIVE
        else:
            return cls.INACTIVE


@dataclass(frozen=True)
class ToggleStyle:
    background_color: Color
    track_color: Color | None = None
    thumb_color: Color | None = None
    border_color: Color | None = None
    border_thickness: int = 0
    text_color: Color | None = None


@dataclass(frozen=True)
class ToggleTheme:
    inactive: ToggleStyle
    active: ToggleStyle | None = None

    def get_for_state(
                self,
                state: ToggleState,
            ) -> ToggleStyle:
        """
        Return the current for state.

        Args:
            state: State used by the operation.

        Returns:
            The current for state.
        """
        if state is ToggleState.ACTIVE and self.active is not None:
            return self.active
        return self.inactive


@dataclass
class ToggleTextConfig:
    text: str = ""
    font: Font | None = None
    color: Color | None = None
    alignment: AlignEnum = AlignEnum.CENTER
    offset_x: int = 0
    offset_y: int = 0
    scale: float = 1.0
    spacing: int = 0
    active_text: str | None = None
    inactive_text: str | None = None
    active_color: Color | None = None
    inactive_color: Color | None = None
    visible_states: set[ToggleState] = field(
        default_factory=lambda: {
            ToggleState.ACTIVE,
            ToggleState.INACTIVE,
        }
    )

    def get_text_for_state(self, state: ToggleState) -> str:
        """
        Return the current text for state.

        Args:
            state: State used by the operation.

        Returns:
            The current text for state.
        """
        if state is ToggleState.ACTIVE and self.active_text is not None:
            return self.active_text
        if state is ToggleState.INACTIVE and self.inactive_text is not None:
            return self.inactive_text
        return self.text

    def get_color_for_state(self, state: ToggleState) -> Color | None:
        """
        Return the current color for state.

        Args:
            state: State used by the operation.

        Returns:
            The current color for state.
        """
        if state is ToggleState.ACTIVE and self.active_color is not None:
            return self.active_color
        if state is ToggleState.INACTIVE and self.inactive_color is not None:
            return self.inactive_color
        return self.color

    def is_visible_for_state(self, state: ToggleState) -> bool:
        """
        Check whether the visible for state condition holds.

        Args:
            state: State used by the operation.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        return state in self.visible_states


class ToggleButton(SuperMesh):
    position: Position
    width: int
    height: int
    active: bool
    layer: MeshLayer
    background: Plane
    track: Plane
    thumb: Plane
    border: Rectangle | None
    theme: ToggleTheme
    texts: list[ToggleTextConfig]
    _text_sequences: list[FontSequence]
    switch_padding: int
    switch_padding_inner: int
    track_width: int
    track_height: int
    thumb_size: int
    switch_side: str

    _action: Callable | None

    def __init__(
                self,
                position: Position,
                width: int,
                height: int,
                inactive_color: Color,
                active_color: Color,
                inactive_track_color: Color | None = None,
                active_track_color: Color | None = None,
                thumb_inactive_color: Color | None = None,
                thumb_active_color: Color | None = None,
                state: ToggleState = ToggleState.INACTIVE,
                operation: OperationEnum = OperationEnum.ALPHA,
                on_click: Callable | None = None,
                border_thickness: int = 0,
                border_color: Color | None = None,
                theme: ToggleTheme | None = None,
                texts: list[ToggleTextConfig] | None = None,
                switch_padding: int = 6,
                switch_padding_inner: int = 4,
                track_width: int | None = None,
                track_height: int | None = None,
                thumb_size: int | None = None,
                switch_side: str = "right",
            ) -> None:
        """
        Initialize the instance.

        Args:
            position: Screen or world coordinates of the object.
            width: Width of the screen or rendered element.
            height: Height of the screen or rendered element.
            inactive_color: Inactive color used by the operation.
            active_color: Active color used by the operation.
            inactive_track_color: Inactive track color used by the operation.
            active_track_color: Active track color used by the operation.
            thumb_inactive_color: Thumb inactive color used by the operation.
            thumb_active_color: Thumb active color used by the operation.
            state: State used by the operation.
            operation: Operation used by the operation.
            on_click: On click used by the operation.
            border_thickness: Border thickness used by the operation.
            border_color: Border color used by the operation.
            theme: Theme used by the operation.
            texts: Texts used by the operation.
            switch_padding: Switch padding used by the operation.
            switch_padding_inner: Switch padding inner used by the operation.
            track_width: Track width used by the operation.
            track_height: Track height used by the operation.
            thumb_size: Thumb size used by the operation.
            switch_side: Switch side used by the operation.
        """
        super().__init__(
            inactive_color,
            operation=operation,
        )

        self._action = on_click

        self.position = position
        self.width = max(1, width)
        self.height = max(1, height)
        self.switch_padding = max(0, switch_padding)
        self.switch_padding_inner = max(0, switch_padding_inner)
        self.track_width = max(
            1,
            track_width or max(28, self.width // 2),
        )
        self.track_height = max(
            1,
            track_height or max(10, self.height - 2 * self.switch_padding),
        )
        self.thumb_size = max(
            6,
            thumb_size
            or max(8, self.track_height - 2 * self.switch_padding_inner),
        )
        self.switch_side = switch_side.lower()
        self.active = state is ToggleState.ACTIVE
        self.layer = MeshLayer()
        self.theme = theme or ToggleTheme(
            inactive=ToggleStyle(
                background_color=inactive_color,
                track_color=inactive_track_color or inactive_color,
                thumb_color=thumb_inactive_color or active_color,
                border_color=border_color or inactive_color,
                border_thickness=border_thickness,
                text_color=None,
            ),
            active=ToggleStyle(
                background_color=active_color,
                track_color=active_track_color or active_color,
                thumb_color=thumb_active_color or inactive_color,
                border_color=(
                    border_color
                    or active_color
                ),
                border_thickness=border_thickness,
                text_color=None,
            ),
        )
        self.texts = texts or []
        self._text_sequences = []

        self.background = Plane(
            self.get_color(),
            (
                self.position,
                Position(
                    self.position.x + self.width,
                    self.position.y + self.height,
                ),
            ),
            operation=self.get_operation(),
            on_click=self._on_click,
        )
        self.layer.meshes.append(self.background)

        self.border = None
        if border_thickness > 0:
            self.border = Rectangle(
                self._current_border_color(),
                self.position,
                self.width,
                self.height,
                border_thickness,
                operation=self.get_operation(),
                smooth_end=True,
            )
            self.layer.meshes.append(self.border)

        self.track = Plane(
            self._current_track_color(),
            (
                self._track_position(),
                Position(
                    self._track_position().x + self.track_width,
                    self._track_position().y + self.track_height,
                ),
            ),
            operation=self.get_operation(),
        )
        self.layer.meshes.append(self.track)

        self.thumb = Plane(
            self._current_thumb_color(),
            (
                self._thumb_position(),
                Position(
                    self._thumb_position().x + self.thumb_size,
                    self._thumb_position().y + self.thumb_size,
                ),
            ),
            operation=self.get_operation(),
        )
        self.layer.meshes.append(self.thumb)

        for text_config in self.texts:
            self.add_text(text_config)

        self.refresh()

    def _on_click(self) -> None:
        """
        Handle on click.
        """
        self.active = not self.active
        self.refresh()

        if self._action:
            self._action(self.active)

    def init(self) -> None:
        """
        Initialize the associated state.
        """
        pass

    def _current_style(self) -> ToggleStyle:
        """
        Handle current style.

        Returns:
            The value produced by the current style operation.
        """
        return self.theme.get_for_state(
            ToggleState.ACTIVE if self.active else ToggleState.INACTIVE,
        )

    def _current_background_color(self) -> Color:
        """
        Handle current background color.

        Returns:
            The value produced by the current background color operation.
        """
        return self._current_style().background_color

    def _current_track_color(self) -> Color:
        """
        Handle current track color.

        Returns:
            The value produced by the current track color operation.
        """
        return (
            self._current_style().track_color
            or self._current_background_color()
        )

    def _current_thumb_color(self) -> Color:
        """
        Handle current thumb color.

        Returns:
            The value produced by the current thumb color operation.
        """
        return (
            self._current_style().thumb_color
            or self._current_background_color()
        )

    def _current_border_color(self) -> Color:
        """
        Handle current border color.

        Returns:
            The value produced by the current border color operation.
        """
        style = self._current_style()
        return style.border_color or self._current_background_color()

    def _track_position(self) -> Position:
        """
        Handle track position.

        Returns:
            The value produced by the track position operation.
        """
        if self.switch_side == "left":
            x = self.position.x + self.switch_padding
        else:
            x = (
                self.position.x + self.width
                - self.track_width - self.switch_padding
            )

        y = self.position.y + ((self.height - self.track_height) // 2)
        return Position(x, y)

    def _thumb_position(self) -> Position:
        """
        Handle thumb position.

        Returns:
            The value produced by the thumb position operation.
        """
        track_origin = self._track_position()
        base_x = track_origin.x + self.switch_padding_inner
        base_y = track_origin.y + ((self.track_height - self.thumb_size) // 2)

        switch_range = max(
            0,
            self.track_width
            - self.thumb_size
            - (2 * self.switch_padding_inner),
        )
        if switch_range <= 0:
            offset_x = 0
        else:
            offset_x = switch_range if self.active else 0

        return Position(base_x + offset_x, base_y)

    def _refresh_texts(self) -> None:
        """
        Handle refresh texts.
        """
        for index, text_config in enumerate(self.texts):
            if index >= len(self._text_sequences):
                continue

            sequence = self._text_sequences[index]
            state = ToggleState.ACTIVE if self.active else ToggleState.INACTIVE
            if not text_config.is_visible_for_state(state):
                sequence.layer.meshes.clear()
                continue

            sequence.position = Position(
                self.position.x + (self.width // 2) + text_config.offset_x,
                self.position.y + (self.height // 2) + text_config.offset_y,
            )
            sequence.set_color(
                text_config.get_color_for_state(state)
                or self._current_style().text_color
                or self._current_background_color()
            )
            sequence.set_sequence_text(
                text_config.get_text_for_state(state)
            )
            sequence.set_operation(self.get_operation())
            sequence.align = text_config.alignment
            sequence.set_scale(text_config.scale)

    def add_text(self, config: ToggleTextConfig) -> FontSequence:
        """
        Add the text to the collection.

        Args:
            config: Configuration values used to initialize the component.

        Returns:
            The value produced by the add text operation.
        """
        if config.font is None:
            raise ValueError(
                "ToggleTextConfig.font is required to render text"
            )

        state = ToggleState.ACTIVE if self.active else ToggleState.INACTIVE
        label = FontSequence(
            config.get_text_for_state(state),
            config.font,
            config.get_color_for_state(state)
            or self._current_style().text_color
            or self._current_background_color(),
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

    def refresh(self) -> None:
        """
        Refresh the rendered state.
        """
        self.background.positions[1].x = self.position.x + self.width
        self.background.positions[1].y = self.position.y + self.height
        self.background.set_color(self._current_background_color())
        self.background.set_operation(self.get_operation())

        if self.border is not None:
            self.border.position = self.position
            self.border.width = self.width
            self.border.height = self.height
            self.border.thickness = self._current_style().border_thickness
            self.border.set_color(self._current_border_color())
            self.border.set_operation(self.get_operation())
            self.border.refresh()

        track_position = self._track_position()
        self.track.positions[0].x = track_position.x
        self.track.positions[0].y = track_position.y
        self.track.positions[1].x = track_position.x + self.track_width
        self.track.positions[1].y = track_position.y + self.track_height
        self.track.set_color(self._current_track_color())
        self.track.set_operation(self.get_operation())

        thumb_position = self._thumb_position()
        self.thumb.positions[0].x = thumb_position.x
        self.thumb.positions[0].y = thumb_position.y
        self.thumb.positions[1].x = thumb_position.x + self.thumb_size
        self.thumb.positions[1].y = thumb_position.y + self.thumb_size
        self.thumb.set_color(self._current_thumb_color())
        self.thumb.set_operation(self.get_operation())

        self._refresh_texts()

    def set_active(self, active: bool) -> None:
        """
        Assign the active.

        Args:
            active: Active used by the operation.
        """
        self.active = active
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
        self.width = max(1, width)
        self.height = max(1, height)
        self.refresh()

    def set_switch_padding(
                self,
                padding: int,
                inner_padding: int | None = None,
            ) -> None:
        """
        Assign the switch padding.

        Args:
            padding: Padding used by the operation.
            inner_padding: Inner padding used by the operation.
        """
        self.switch_padding = max(0, padding)
        if inner_padding is not None:
            self.switch_padding_inner = max(0, inner_padding)
        self.refresh()

    def set_switch_padding_inner(self, padding: int) -> None:
        """
        Assign the switch padding inner.

        Args:
            padding: Padding used by the operation.
        """
        self.switch_padding_inner = max(0, padding)
        self.refresh()

    def set_track_size(self, width: int, height: int) -> None:
        """
        Assign the track size.

        Args:
            width: Width of the screen or rendered element.
            height: Height of the screen or rendered element.
        """
        self.track_width = max(1, width)
        self.track_height = max(1, height)
        self.refresh()

    def set_thumb_size(self, size: int) -> None:
        """
        Assign the thumb size.

        Args:
            size: Size value to convert or apply.
        """
        self.thumb_size = max(6, size)
        self.refresh()

    def set_switch_side(self, side: str) -> None:
        """
        Assign the switch side.

        Args:
            side: Side used by the operation.
        """
        self.switch_side = side.lower()
        self.refresh()

    def set_theme(self, theme: ToggleTheme) -> None:
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
        self.background.set_operation(operation)
        self.track.set_operation(operation)
        self.thumb.set_operation(operation)
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
        self.background.set_color(color)
