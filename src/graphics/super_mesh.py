from abc import ABC, abstractmethod

from .mesh import Mesh
from .mesh_layer import MeshLayer


class SuperMesh(Mesh, ABC):
    @abstractmethod
    def get_layer(self) -> MeshLayer:
        ...

    @abstractmethod
    def init(self) -> None:
        ...

    @abstractmethod
    def refresh(self) -> None:
        ...
