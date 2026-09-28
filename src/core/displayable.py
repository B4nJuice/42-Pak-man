from abc import ABC, abstractmethod
from typing import Any

from ..graphics import Mesh


class Displayable(ABC):
    _mesh: Mesh

    def __init__(
                self,
                *args: Any,
                **kwargs: Any
            ) -> None:
        super().__init__(*args, **kwargs)
        self.init_mesh()

    @abstractmethod
    def init_mesh(self) -> None:
        pass

    def get_mesh(self) -> Mesh:
        return self._mesh

    @abstractmethod
    def update_mesh(self) -> None:
        pass
