from collections.abc import Callable


class Timer:
    _value: float
    _speed: float
    _cb_update: Callable[[float], None] | None
    _cb_finish: Callable[[], None] | None

    def __init__(self, value: float, speed: float = 1.0) -> None:
        self.set(value)
        self.set_speed(speed)
        self.set_cb_update(None)
        self.set_cb_finish(None)

    def set_cb_update(self, cb: Callable[[float], None] | None) -> None:
        self._cb_update = cb

    def set_cb_finish(self, cb: Callable[[], None] | None) -> None:
        self._cb_finish = cb

    def set(self, value: float) -> None:
        self._value = value

    def set_speed(self, value: float) -> None:
        self._speed = value

    def update(self, dt: float) -> None:
        if self._value <= 0.0:
            return

        self._value = self._value - (dt * self._speed)
        if self._value <= 0.0 and self._cb_finish is not None:
            self._cb_finish()

        if self._cb_update is not None:
            self._cb_update(self._value)
