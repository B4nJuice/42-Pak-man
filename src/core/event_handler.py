from collections.abc import Callable

from pygame.event import Event

listener = Callable[[Event, int], None]


class EventHandler:
    _listeners: dict[int, list[listener]]

    def __init__(self) -> None:
        """
        Initialize the instance.
        """
        self._listeners = {}

    def dispatch_event(self, event: Event, event_type: int) -> None:
        """
        Handle dispatch event.

        Args:
            event: Pygame event being handled.
            event_type: Event type used by the operation.
        """
        if event_type in self._listeners:
            for listener in self._listeners[event_type]:
                listener(event, event_type)

    def register_listener(self, event_type: int, listener: listener) -> None:
        """
        Handle register listener.

        Args:
            event_type: Event type used by the operation.
            listener: Listener used by the operation.
        """
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)
