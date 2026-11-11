from collections.abc import Callable


class Timer:
    _value: float
    _speed: float
    _cb_update: Callable[[float], None] | None
    _cb_finish: Callable[[], None] | None

    def __init__(self, value: float, speed: float = 1.0) -> None:
        """
        Initialize the instance.

        Args:
            value: Value to assign or apply.
            speed: Speed used by the operation.
        """
        self.set(value)
        self.set_speed(speed)
        self.set_cb_update(None)
        self.set_cb_finish(None)

    def set_cb_update(self, cb: Callable[[float], None] | None) -> None:
        """
        Assign the cb update.

        Args:
            cb: Cb used by the operation.
        """
        self._cb_update = cb

    def set_cb_finish(self, cb: Callable[[], None] | None) -> None:
        """
        Assign the cb finish.

        Args:
            cb: Cb used by the operation.
        """
        self._cb_finish = cb

    def set(self, value: float) -> None:
        """
        Handle set.

        Args:
            value: Value to assign or apply.
        """
        self._value = value

    def add_time(self, value: float) -> None:
        """
        Add the time to the collection.

        Args:
            value: Value to assign or apply.
        """
        self._value += value

    def remove_time(self, value: float) -> None:
        """
        Remove the time from the collection.

        Args:
            value: Value to assign or apply.
        """
        self._value = max(self._value - value, 0.0)

    def set_speed(self, value: float) -> None:
        """
        Assign the speed.

        Args:
            value: Value to assign or apply.
        """
        self._speed = value

    def get_speed(self) -> float:
        """
        Return the current speed.

        Returns:
            The current speed.
        """
        return self._speed

    def get(self) -> float:
        """
        Handle get.

        Returns:
            The value produced by the get operation.
        """
        return self._value

    def update(self, dt: float) -> None:
        """
        Handle update.

        Args:
            dt: Elapsed time since the previous update, in seconds.
        """
        if self._value <= 0.0:
            return

        self._value = self._value - (dt * self._speed)
        if self._value <= 0.0 and self._cb_finish is not None:
            self._cb_finish()

        if self._cb_update is not None:
            self._cb_update(self._value)
