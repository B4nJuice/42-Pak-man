from typing import Any

from .entity import Entity


class Alive:
    _initial_max_health: int
    _initial_health: int
    _max_health: int
    _health: int
    _lives: int

    def __init__(
                self,
                *args: Any,
                health: int = 1,
                max_health: int = 1,
                lives: int = 1,
                **kwargs: Any
            ) -> None:
        super().__init__(*args, **kwargs)

        if not isinstance(self, Entity):
            raise TypeError(
                f'Alive must be a subclass of Entity, got {type(self)}'
            )

        self.set_health(health)
        self.set_max_health(max_health)
        self.set_lives(lives)
        self._initial_health = self.get_health()
        self._initial_max_health = self.get_max_health()

    def set_health(self, health: int) -> None:
        self._health = max(0, health)

    def set_max_health(self, max_health: int) -> None:
        self._max_health = max(1, max_health)

    def set_lives(self, lives: int) -> None:
        self._lives = max(0, lives)

    def get_health(self) -> int:
        return self._health

    def get_max_health(self) -> int:
        return self._max_health

    def get_lives(self) -> int:
        return self._lives

    def add_health(self, amount: int) -> None:
        self.set_health(self.get_health() + amount)

    def add_max_health(self, amount: int) -> None:
        self.set_max_health(self.get_max_health() + amount)

    def add_lives(self, amount: int) -> None:
        self.set_lives(self.get_lives() + amount)

    @property
    def alive(self) -> bool:
        return self.get_health() > 0

    @property
    def over(self) -> bool:
        return self.get_lives() <= 0

    def on_death(self) -> None:
        self.add_lives(-1)
        self.set_health(self.get_max_health())
