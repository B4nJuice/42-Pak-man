from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.game.characters import Player

from .entity import Entity


class Edible:
    _reward: float
    _edible: bool

    def __init__(
                self,
                *args: Any,
                reward: float = 0,
                edible: bool = True,
                **kwargs: Any
            ) -> None:
        """
        Initialize the instance.

        Args:
            reward: Reward used by the operation.
            edible: Edible used by the operation.
            args: Command-line arguments passed to the application.
            kwargs: Kwargs used by the operation.
        """
        super().__init__(*args, **kwargs)

        if not isinstance(self, Entity):
            raise TypeError(
                f'Edible must be a subclass of Entity, got {type(self)}'
            )

        self._reward = reward
        self.set_edible(edible)

    def get_reward(self) -> float:
        """
        Return the current reward.

        Returns:
            The current reward.
        """
        return self._reward

    def set_edible(self, value: bool) -> None:
        """
        Assign the edible.

        Args:
            value: Value to assign or apply.
        """
        self._edible = value

    def eat(self, eater: 'Player') -> bool:
        """
        Handle eat.

        Args:
            eater: Eater used by the operation.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        if not self._edible:
            return False

        if not isinstance(self, Entity):
            return False

        eater.add_exp(self.get_reward())
        return True
