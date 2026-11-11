from abc import ABC, abstractmethod
from typing import Any

from src.app import App
from src.core.entity import Entity
from src.graphics.position import Position
from src.texture.animation_player import AnimationPlayer
from src.texture.texture_frame import TextureFrame
from src.texture.texture_keys import TextureKeys


class Displayable(ABC):
    _rotation: float
    _proportion: float
    _hidden: bool
    _mesh_level_position: Position
    _tile_height: int
    _tile_width: int

    def __init__(
                self,
                *args: Any,
                proportion: float = 1.0,
                rotation: float = 0.0,
                **kwargs: Any
            ) -> None:
        """
        Initialize the instance.

        Args:
            proportion: Proportion used by the operation.
            rotation: Rotation used by the operation.
            args: Command-line arguments passed to the application.
            kwargs: Kwargs used by the operation.
        """
        super().__init__(*args, **kwargs)

        self.set_hidden(False)
        self._proportion = proportion
        self._rotation = rotation
        self.init_displayable()

    def set_hidden(self, hidden: bool) -> None:
        """
        Assign the hidden.

        Args:
            hidden: Hidden used by the operation.
        """
        self._hidden = hidden

    def is_hidden(self) -> bool:
        """
        Check whether the hidden condition holds.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        return self._hidden

    def set_tile_size(self, height: int, width: int) -> None:
        """
        Assign the tile size.

        Args:
            height: Height of the screen or rendered element.
            width: Width of the screen or rendered element.
        """
        self._tile_height = height
        self._tile_width = width

    def set_mesh_level_position(self, pos: Position) -> None:
        """
        Assign the mesh level position.

        Args:
            pos: Pos used by the operation.
        """
        self._mesh_level_position = pos

    def get_position_on_screen(self) -> Position:
        """
        Return the current position on screen.

        Returns:
            The current position on screen.
        """
        if not isinstance(self, Entity):
            raise TypeError(
                f'Displayable must be a subclass of Entity, got {type(self)}'
            )

        return Position(
            round(
                self.pos[0]
                * self._tile_width
                + self._mesh_level_position.x
                + self._tile_width // 2
            ),
            round(
                self.pos[1]
                * self._tile_height
                + self._mesh_level_position.y
                + self._tile_height // 2
            )
        )

    def get_width(self) -> int:
        """
        Return the current width.

        Returns:
            The current width.
        """
        return round(
            self._tile_width * self.get_proportion()
        )

    def get_height(self) -> int:
        """
        Return the current height.

        Returns:
            The current height.
        """
        return round(
            self._tile_height * self.get_proportion()
        )

    @abstractmethod
    def init_displayable(self) -> None:
        """
        Initialize the associated state.
        """
        pass

    def get_rotation(self) -> float:
        """
        Return the current rotation.

        Returns:
            The current rotation.
        """
        return self._rotation

    def set_rotation(self, rotation: float) -> None:
        """
        Assign the rotation.

        Args:
            rotation: Rotation used by the operation.
        """
        self._rotation = rotation

    def get_proportion(self) -> float:
        """
        Return the current proportion.

        Returns:
            The current proportion.
        """
        return self._proportion

    def set_proportion(self, proportion: float) -> None:
        """
        Assign the proportion.

        Args:
            proportion: Proportion used by the operation.
        """
        self._proportion = proportion

    @abstractmethod
    def get_animation(self) -> AnimationPlayer:
        """
        Return the current animation.

        Returns:
            The current animation.
        """
        pass

    def get_texture(self) -> TextureFrame:
        """
        Return the current texture.

        Returns:
            The current texture.
        """
        return self.get_animation().frame

    def update_animation(self, dt: float) -> None:
        """
        Update the animation.

        Args:
            dt: Elapsed time since the previous update, in seconds.
        """
        self.get_animation().update(dt)


class SimpleDisplayable(Displayable):
    _width: int
    _height: int
    _position: Position
    _app: App
    _texture_key: str

    def __init__(
        self,
        app: App | None = None,
        texture_key: str | TextureKeys | None = None,
        width: int | None = None,
        height: int | None = None,
        position: Position | None = None,
    ) -> None:
        """
        Initialize the instance.

        Args:
            app: Application instance that owns the object.
            texture_key: Texture key used by the operation.
            width: Width of the screen or rendered element.
            height: Height of the screen or rendered element.
            position: Screen or world coordinates of the object.
        """
        if (
            app is None
            or texture_key is None
            or width is None
            or height is None
            or position is None
        ):
            raise TypeError(
                'SimpleDisplayable requires app, texture, size and position'
            )
        self.set_app(app)
        self.set_texture_key(texture_key)
        self.set_width(width)
        self.set_height(height)
        self.set_position(position)
        super().__init__()

    def set_app(self, app: App) -> None:
        """
        Assign the app.

        Args:
            app: Application instance that owns the object.
        """
        self._app = app

    def set_width(self, width: int) -> None:
        """
        Assign the width.

        Args:
            width: Width of the screen or rendered element.
        """
        self._width = width

    def set_height(self, height: int) -> None:
        """
        Assign the height.

        Args:
            height: Height of the screen or rendered element.
        """
        self._height = height

    def get_width(self) -> int:
        """
        Return the current width.

        Returns:
            The current width.
        """
        return self._width

    def get_height(self) -> int:
        """
        Return the current height.

        Returns:
            The current height.
        """
        return self._height

    def set_position(self, pos: Position) -> None:
        """
        Assign the position.

        Args:
            pos: Pos used by the operation.
        """
        self._position = pos

    def get_position_on_screen(self) -> Position:
        """
        Return the current position on screen.

        Returns:
            The current position on screen.
        """
        return self._position

    def set_texture_key(self, texture_key: str | TextureKeys) -> None:
        """
        Assign the texture key.

        Args:
            texture_key: Texture key used by the operation.
        """
        if isinstance(texture_key, TextureKeys):
            self._texture_key = texture_key.str()
        else:
            self._texture_key = texture_key

        if hasattr(self, '_animation'):
            self.init_displayable()

    def get_texture_key(self) -> str:
        """
        Return the current texture key.

        Returns:
            The current texture key.
        """
        return self._texture_key

    def init_displayable(self) -> None:
        """
        Initialize the associated state.
        """
        self._animation = AnimationPlayer(
            self._app.texture.get(TextureKeys.get(self._texture_key))
        )

    def get_animation(self) -> AnimationPlayer:
        """
        Return the current animation.

        Returns:
            The current animation.
        """
        return self._animation


class DisplayableEntity(Displayable, Entity):
    """Structural equivalent of Displayable & Entity."""
