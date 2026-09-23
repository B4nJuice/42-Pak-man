from abc import ABC, abstractmethod

from ..graphics import Mesh


class Displayable(ABC):
    _mesh: Mesh

    def __init__(
                self,
                *args,
                **kwargs
            ) -> None:
        super().__init__(*args, **kwargs)

    @abstractmethod
    def get_mesh(self) -> Mesh:
        pass

    @abstractmethod
    def update_mesh(self) -> None:
        pass
