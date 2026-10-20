from abc import ABC, abstractmethod
from typing import Any

from src.core.entity import Entity
from src.graphics.position import Position
from src.texture.animation_player import AnimationPlayer
from src.texture.texture_frame import TextureFrame


class Displayable(ABC):
    _rotation: float
    _proportion: float

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

        self._proportion = proportion
        self._rotation = rotation
        self.init_displayable()

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


class DisplayableEntity(Displayable, Entity):
    """Structural equivalent of Displayable & Entity."""
