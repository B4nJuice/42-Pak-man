from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from src.graphics.mesh import Mesh


class Clickable(ABC):
    _on_click: Callable | None = None

    def __init__(
                self,
                on_click: Callable | None = None,
                on_hover: Callable | None = None,
                *args: Any,
                **kwargs: Any
            ) -> None:
        if not isinstance(self, Mesh):
            raise TypeError(
                f'Clickable must be a subclass of Mesh, got {type(self)}'
            )

        super().__init__(*args, **kwargs)
        self._on_click = on_click
        self._on_hover = on_hover

    @abstractmethod
    def contains(self, x: int, y: int) -> bool:
        pass

    def hover(self, x: int, y: int, *args: Any, **kwargs: Any) -> Any:
        if self._on_hover and self.contains(x, y):
            return self._on_hover(*args, **kwargs)

    def click(self, x: int, y: int, *args: Any, **kwargs: Any) -> Any:
        if self._on_click and self.contains(x, y):
            return self._on_click(*args, **kwargs)
