from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..graphics import Mesh


class MeshLayer:
    def __init__(self) -> None:
        self.meshes: list[Mesh | 'MeshLayer'] = []

    def get_layer(self) -> 'MeshLayer':
        return self
