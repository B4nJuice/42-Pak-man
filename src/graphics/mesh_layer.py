from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from src.core import Displayable

    from ..graphics import Mesh


class MeshLayer:
    meshes: list['Mesh | LayerProtocol | Displayable']
    hidden: bool

    def __init__(self) -> None:
        """
        Initialize the instance.
        """
        self.meshes = []
        self.hidden = False

    def get_layer(self) -> 'MeshLayer':
        """
        Return the current layer.

        Returns:
            The current layer.
        """
        return self

    def is_hidden(self) -> bool:
        """
        Check whether the hidden condition holds.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        return self.hidden


@runtime_checkable
class LayerProtocol(Protocol):
    def get_layer(self) -> MeshLayer:
        """
        Return the current layer.

        Returns:
            The current layer.
        """
        ...

    def is_hidden(self) -> bool:
        """
        Check whether the hidden condition holds.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        ...
