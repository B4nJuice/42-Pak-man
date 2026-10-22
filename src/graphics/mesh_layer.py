from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from src.core import Displayable

    from ..graphics import Mesh


class MeshLayer:
    meshes: list['Mesh | LayerProtocol | Displayable']

    def __init__(self) -> None:
        self.meshes = []

    def get_layer(self) -> 'MeshLayer':
        return self


@runtime_checkable
class LayerProtocol(Protocol):
    def get_layer(self) -> MeshLayer:
        pass
