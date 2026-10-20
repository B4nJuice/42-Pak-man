from .color import Color, OperationEnum
from .mesh import Mesh
from .clickable import Clickable
from .meshes import Character, Circle, ImageTexture, Line, Plane, Polygon
from .position import Position
from .mesh_layer import MeshLayer
from .super_mesh import SuperMesh

__all__: list[str] = [
    'Character',
    'Circle',
    'Color',
    'ImageTexture',
    'Line',
    'Mesh',
    'MeshLayer',
    'OperationEnum',
    'Plane',
    'Polygon',
    'Position',
    'Screen',
    'SuperMesh',
    'Clickable'
]


def __getattr__(name: str) -> object:
    if name == 'Screen':
        from src.graphics.screen import Screen

        return Screen
    raise AttributeError(f"module 'src.graphics' has no attribute {name!r}")
