from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from src.graphics.mesh_layer import MeshLayer

if TYPE_CHECKING:
    from src.game.game import Game


class Interface(ABC):
    hidden: bool

    def __init__(self, game: 'Game') -> None:
        """
        Initialize the instance.

        Args:
            game: Game instance associated with the component.
        """
        self.hidden = False

    def is_hidden(self) -> bool:
        """
        Check whether the hidden condition holds.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        return self.hidden

    def hide(self) -> None:
        """
        Handle hide.
        """
        self.hidden = True

    def display(self) -> None:
        """
        Display the interface contents.
        """
        self.hidden = False

    def handle_key(self, key: int) -> bool:
        """
        Handle handle key.

        Args:
            key: Keyboard key code associated with the action.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        return False

    @abstractmethod
    def get_layer(self) -> MeshLayer:
        """
        Return the current layer.

        Returns:
            The current layer.
        """
        ...
