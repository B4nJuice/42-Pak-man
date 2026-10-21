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
        super().__init__(*args, **kwargs)

        self.set_hidden(False)
        self._proportion = proportion
        self._rotation = rotation
        self.init_displayable()

    def set_hidden(self, hidden: bool) -> None:
        self._hidden = hidden

    def is_hidden(self) -> bool:
        return self._hidden

    def set_tile_size(self, height: int, width: int) -> None:
        self._tile_height = height
        self._tile_width = width

    def set_mesh_level_position(self, pos: Position) -> None:
        self._mesh_level_position = pos

    def get_position_on_screen(self) -> Position:
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
        return round(
            self._tile_width * self.get_proportion()
        )

    def get_height(self) -> int:
        return round(
            self._tile_height * self.get_proportion()
        )

    @abstractmethod
    def init_displayable(self) -> None:
        pass

    def get_rotation(self) -> float:
        return self._rotation

    def set_rotation(self, rotation: float) -> None:
        self._rotation = rotation

    def get_proportion(self) -> float:
        return self._proportion

    def set_proportion(self, proportion: float) -> None:
        self._proportion = proportion

    @abstractmethod
    def get_animation(self) -> AnimationPlayer:
        pass

    def get_texture(self) -> TextureFrame:
        return self.get_animation().frame

    def update_animation(self, dt: float) -> None:
        self.get_animation().update(dt)


class SimpleDisplayable(Displayable, ABC):
    _width: int
    _height: int
    _position: Position
    _app: App
    _texture_key: str

    def set_app(self, app: App) -> None:
        self._app = app

    def set_width(self, width: int) -> None:
        self._width = width

    def set_height(self, height: int) -> None:
        self._height = height

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    def set_position(self, pos: Position) -> None:
        self._position = pos

    def get_position_on_screen(self) -> Position:
        return self._position

    def set_texture_key(self, texture_key: str) -> None:
        self._texture_key = texture_key

    def init_displayable(self) -> None:
        self._animation = AnimationPlayer(
            self._app.texture.get(TextureKeys.get(self._texture_key))
        )

    def get_animation(self) -> AnimationPlayer:
        return self._animation


class DisplayableEntity(Displayable, Entity):
    """Structural equivalent of Displayable & Entity."""
