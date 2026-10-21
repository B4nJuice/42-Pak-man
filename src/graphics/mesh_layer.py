from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.displayable import Displayable

    from ..graphics import Mesh


class MeshLayer:
    meshes: list['Mesh | MeshLayer | Displayable']

    def __init__(self) -> None:
        self.meshes = []

    def get_layer(self) -> 'MeshLayer':
        return self
