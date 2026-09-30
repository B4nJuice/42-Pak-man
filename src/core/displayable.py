from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..graphics.mesh import Mesh



class Displayable(ABC):
    _mesh: 'Mesh'
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

    def get_mesh(self) -> 'Mesh':
        return self._mesh

    def get_rotation(self) -> float:
        return self._rotation

    def set_rotation(self, rotation: float) -> None:
        self._rotation = rotation

    def get_proportion(self) -> float:
        return self._proportion

    def set_proportion(self, proportion: float) -> None:
        self._proportion = proportion

    @abstractmethod
    def update_mesh(self) -> None:
        pass
