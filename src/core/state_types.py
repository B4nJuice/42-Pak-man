from abc import ABC, abstractmethod
from collections.abc import Callable


class Updatable(ABC):
    @abstractmethod
    def update(self, dt: float) -> None:
        """
        Handle update.

        Args:
            dt: Elapsed time since the previous update, in seconds.
        """
        pass


class CooldownState(Updatable):
    _default_value: float
    _value: float
    _callback_expire: list[Callable]

    def __init__(self, default: float = 0.0, value: float = 0.0) -> None:
        """
        Initialize the instance.

        Args:
            default: Default used by the operation.
            value: Value to assign or apply.
        """
        self.set(value)
        self.set_default_value(default)
        self._callback_expire = []

    def update(self, dt: float) -> None:
        """
        Handle update.

        Args:
            dt: Elapsed time since the previous update, in seconds.
        """
        if self._value > 0.0:
            self._value -= dt

            if self.has_exipred():
                self.on_expire()

    def set(self, value: float) -> None:
        """
        Handle set.

        Args:
            value: Value to assign or apply.
        """
        self._value = value

    def set_default(self) -> None:
        """
        Assign the default.
        """
        self.set(self._default_value)

    def get_default(self) -> float:
        """
        Return the current default.

        Returns:
            The current default.
        """
        return self._default_value

    def set_default_value(self, value: float) -> None:
        """
        Assign the default value.

        Args:
            value: Value to assign or apply.
        """
        self._default_value = value

    def get(self) -> float:
        """
        Handle get.

        Returns:
            The value produced by the get operation.
        """
        return self._value

    def is_active(self) -> bool:
        """
        Check whether the active condition holds.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        return self.get() > 0.0

    def has_exipred(self) -> bool:
        """
        Check whether the  exipred condition holds.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        return self.get() <= 0.0

    def on_expire(self) -> None:
        """
        Handle the expire event.
        """
        for cb in self._callback_expire:
            cb()

    def register_callback(self, cb: Callable) -> None:
        """
        Handle register callback.

        Args:
            cb: Cb used by the operation.
        """
        self._callback_expire.append(cb)

    @property
    def active(self) -> bool:
        """
        Handle active.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        return self.is_active()
