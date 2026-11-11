from abc import ABC, abstractmethod

from .mesh import Mesh
from .mesh_layer import MeshLayer


class SuperMesh(Mesh, ABC):
    @abstractmethod
    def get_layer(self) -> MeshLayer:
        """
        Return the current layer.

        Returns:
            The current layer.
        """
        ...

    @abstractmethod
    def init(self) -> None:
        """
        Initialize the associated state.
        """
        ...

    @abstractmethod
    def refresh(self) -> None:
        """
        Refresh the rendered state.
        """
        ...
