from typing import Any, TYPE_CHECKING

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
        super().__init__(*args, **kwargs)

        if not isinstance(self, Entity):
            raise TypeError(
                f'Edible must be a subclass of Entity, got {type(self)}'
            )

        self._reward = reward
        self.set_edible(edible)

    def get_reward(self) -> float:
        return self._reward

    def set_edible(self, value: bool) -> None:
        self._edible = value

    def eat(self, eater: 'Player') -> bool:
        if not self._edible:
            return False

        if not isinstance(self, Entity):
            return False

        eater.add_exp(self.get_reward())
        self.level.unregister_entity(self)
        return True
