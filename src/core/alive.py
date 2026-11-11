from typing import Any

from .entity import Entity


class Alive:
    _initial_max_health: int
    _initial_health: int
    _max_health: int
    _max_lives: int
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
        """
        Initialize the instance.

        Args:
            health: Health used by the operation.
            max_health: Max health used by the operation.
            lives: Lives used by the operation.
            args: Command-line arguments passed to the application.
            kwargs: Kwargs used by the operation.
        """
        super().__init__(*args, **kwargs)

        if not isinstance(self, Entity):
            raise TypeError(
                f'Alive must be a subclass of Entity, got {type(self)}'
            )

        self.set_health(health)
        self.set_max_health(max_health)
        self.set_lives(lives)
        self.set_max_lives(lives)
        self._initial_health = self.get_health()
        self._initial_max_health = self.get_max_health()

    def set_health(self, health: int) -> None:
        """
        Assign the health.

        Args:
            health: Health used by the operation.
        """
        self._health = max(0, health)

    def set_max_health(self, max_health: int) -> None:
        """
        Assign the max health.

        Args:
            max_health: Max health used by the operation.
        """
        self._max_health = max(1, max_health)

    def set_lives(self, lives: int) -> None:
        """
        Assign the lives.

        Args:
            lives: Lives used by the operation.
        """
        self._lives = max(0, lives)

    def set_max_lives(self, max_lives: int) -> None:
        """
        Assign the max lives.

        Args:
            max_lives: Max lives used by the operation.
        """
        self._max_lives = max(1, max_lives)

    def get_health(self) -> int:
        """
        Return the current health.

        Returns:
            The current health.
        """
        return self._health

    def get_max_health(self) -> int:
        """
        Return the current max health.

        Returns:
            The current max health.
        """
        return self._max_health

    def get_lives(self) -> int:
        """
        Return the current lives.

        Returns:
            The current lives.
        """
        return self._lives

    def add_health(self, amount: int) -> None:
        """
        Add the health to the collection.

        Args:
            amount: Amount used by the operation.
        """
        self.set_health(self.get_health() + amount)

    def add_max_health(self, amount: int) -> None:
        """
        Add the max health to the collection.

        Args:
            amount: Amount used by the operation.
        """
        self.set_max_health(self.get_max_health() + amount)

    def add_lives(self, amount: int) -> None:
        """
        Add the lives to the collection.

        Args:
            amount: Amount used by the operation.
        """
        self.set_lives(self.get_lives() + amount)

    @property
    def alive(self) -> bool:
        """
        Handle alive.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        return self.get_health() > 0

    @property
    def over(self) -> bool:
        """
        Handle over.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        return self.get_lives() <= 0

    def on_death(self) -> None:
        """
        Handle the death event.
        """
        self.add_lives(-1)
        self.set_health(self.get_max_health())
