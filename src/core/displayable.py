from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..graphics.meshes import ImageTexture



class Displayable(ABC):
    _mesh: 'ImageTexture'
    _rotation: float
    _proportion: float

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
        self.init_mesh()

    @abstractmethod
    def init_mesh(self) -> None:
        pass

    def get_mesh(self) -> 'ImageTexture':
        return self._mesh

    def get_rotation(self) -> float:
        return self._rotation

    def set_rotation(self, rotation: float) -> None:
        self._rotation = rotation

    def get_proportion(self) -> float:
        return self._proportion

    def set_proportion(self, proportion: float) -> None:
        self._proportion = proportion

    def get_texture(self) -> Any:
        return self._mesh.texture

    def update_mesh(self) -> None:
        self._mesh.image = self.get_texture().image
        self._mesh.texture = self.get_texture().texture