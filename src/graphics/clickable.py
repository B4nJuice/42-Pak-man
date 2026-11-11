from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from src.graphics.mesh import Mesh
from src.graphics.mesh_layer import LayerProtocol


class Clickable(Mesh, ABC):
    _on_click: Callable | None = None
    _parents: list[LayerProtocol]

    def __init__(
                self,
                on_click: Callable | None = None,
                on_hover: Callable | None = None,
                *args: Any,
                **kwargs: Any
            ) -> None:
        """
        Initialize the instance.

        Args:
            on_click: On click used by the operation.
            on_hover: On hover used by the operation.
            args: Command-line arguments passed to the application.
            kwargs: Kwargs used by the operation.
        """
        self._parents = []

        super().__init__(*args, **kwargs)
        self._on_click = on_click
        self._on_hover = on_hover

    @abstractmethod
    def contains(self, x: int, y: int) -> bool:
        """
        Handle contains.

        Args:
            x: Horizontal coordinate or value.
            y: Vertical coordinate or value.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        pass

    def set_parents(self, parents: list[LayerProtocol]) -> None:
        """
        Assign the parents.

        Args:
            parents: Parent meshes used to preserve the element hierarchy.
        """
        self._parents = parents

    def is_hidden(self) -> bool:
        """
        Check whether the hidden condition holds.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        return any(p.is_hidden() for p in self._parents) or super().is_hidden()

    def hover(self, x: int, y: int, *args: Any, **kwargs: Any) -> Any:
        """
        Handle hover.

        Args:
            x: Horizontal coordinate or value.
            y: Vertical coordinate or value.
            args: Command-line arguments passed to the application.
            kwargs: Kwargs used by the operation.

        Returns:
            The value produced by the hover operation.
        """
        if not self.is_hidden() and self._on_hover and self.contains(x, y):
            return self._on_hover(*args, **kwargs)

    def click(self, x: int, y: int, *args: Any, **kwargs: Any) -> Any:
        """
        Handle click.

        Args:
            x: Horizontal coordinate or value.
            y: Vertical coordinate or value.
            args: Command-line arguments passed to the application.
            kwargs: Kwargs used by the operation.

        Returns:
            The value produced by the click operation.
        """
        if not self.is_hidden() and self._on_click and self.contains(x, y):
            return self._on_click(*args, **kwargs)

    def sim_click(self, *args: Any, **kwargs: Any) -> Any:
        """
        Handle sim click.

        Args:
            args: Command-line arguments passed to the application.
            kwargs: Kwargs used by the operation.

        Returns:
            The value produced by the sim click operation.
        """
        if self._on_click:
            return self._on_click(*args, **kwargs)
