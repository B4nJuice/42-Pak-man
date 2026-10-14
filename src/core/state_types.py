from abc import ABC, abstractmethod
from collections.abc import Callable


class Updatable(ABC):
    @abstractmethod
    def update(self, dt: float) -> None:
        pass


class CooldownState(Updatable):
    _default_value: float
    _value: float
    _callback_expire: list[Callable]

    def __init__(self, default: float = 0.0, value: float = 0.0) -> None:
        self.set(value)
        self.set_default_value(default)
        self._callback_expire = []

    def update(self, dt: float) -> None:
        if self._value > 0.0:
            self._value -= dt

            if self.has_exipred():
                self.on_expire()

    def set(self, value: float) -> None:
        self._value = value

    def set_default(self) -> None:
        self.set(self._default_value)

    def get_default(self) -> float:
        return self._default_value

    def set_default_value(self, value: float) -> None:
        self._default_value = value

    def get(self) -> float:
        return self._value

    def is_active(self) -> bool:
        return self.get() > 0.0

    def has_exipred(self) -> bool:
        return self.get() <= 0.0

    def on_expire(self) -> None:
        for cb in self._callback_expire:
            cb()

    def register_callback(self, cb: Callable) -> None:
        self._callback_expire.append(cb)

    @property
    def active(self) -> bool:
        return self.is_active()
