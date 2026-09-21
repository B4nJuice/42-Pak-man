from abc import ABC, abstractmethod

from src.graphics import Mesh, MeshLayer

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