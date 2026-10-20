from typing import TYPE_CHECKING

from src.core.displayable import DisplayableEntity

if TYPE_CHECKING:
    from ..graphics import Mesh


class MeshLayer:
    meshes: list['Mesh | MeshLayer | DisplayableEntity']

    def __init__(self) -> None:
        self.meshes = []

    def get_layer(self) -> 'MeshLayer':
        return self
