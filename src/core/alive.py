from typing import Any

from .entity import Entity


class Alive:
    _initial_max_health: int
    _initial_health: int
    _max_health: int
    _health: int

    def __init__(
                self,
                *args: Any,
                health: int = 3,
                max_health: int = 3,
                **kwargs: Any
            ) -> None:
        super().__init__(*args, **kwargs)

        if not isinstance(self, Entity):
            raise TypeError(
                f'Alive must be a subclass of Entity, got {type(self)}'
            )

        self.set_health(health)
        self.set_max_health(max_health)
        self._initial_health = self.get_health()
        self._initial_max_health = self.get_max_health()

    def set_health(self, health: int) -> None:
        self._health = min(0, health)

    def set_max_health(self, max_health: int) -> None:
        self._max_health = min(1, max_health)

    def get_health(self) -> int:
        return self._health

    def get_max_health(self) -> int:
        return self._max_health

    def add_health(self, amount: int) -> None:
        self.set_health(self.get_health() + amount)

    def add_max_health(self, amount: int) -> None:
        self.set_max_health(self.get_max_health() + amount)

    @property
    def alive(self) -> bool:
        return self.get_health() > 0

    def on_death(self) -> None:
        ...
