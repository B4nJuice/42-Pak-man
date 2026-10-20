from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from src.graphics import Mesh


class Clickable(ABC):
    _on_click: Callable | None = None

    def __init__(
                self,
                on_click: Callable | None = None,
                *args: Any,
                **kwargs: Any
            ) -> None:
        if not isinstance(self, Mesh):
            raise TypeError(
                f'Clickable must be a subclass of Mesh, got {type(self)}'
            )

        super().__init__(*args, **kwargs)
        self._on_click = on_click

    @abstractmethod
    def contains(self, x: int, y: int) -> bool:
        pass

    def click(self, x: int, y: int, *args: Any, **kwargs: Any) -> Any:
        if self._on_click and self.contains(x, y):
            self._on_click(*args, **kwargs)
