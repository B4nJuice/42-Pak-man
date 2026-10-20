from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.displayable import DisplayableEntity

    from ..graphics import Mesh


class MeshLayer:
    meshes: list['Mesh | MeshLayer | DisplayableEntity']

    def __init__(self) -> None:
        self.meshes = []

    def get_layer(self) -> 'MeshLayer':
        return self
