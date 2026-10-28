from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from src.core import Displayable

    from ..graphics import Mesh


class MeshLayer:
    meshes: list['Mesh | LayerProtocol | Displayable']
    hidden: bool

    def __init__(self) -> None:
        self.meshes = []
        self.hidden = False

    def get_layer(self) -> 'MeshLayer':
        return self

    def is_hidden(self) -> bool:
        return self.hidden


@runtime_checkable
class LayerProtocol(Protocol):
    def get_layer(self) -> MeshLayer:
        ...

    def is_hidden(self) -> bool:
        ...
