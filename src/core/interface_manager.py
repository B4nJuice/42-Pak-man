from typing import TYPE_CHECKING

from src.game.game_status import InterfaceStatus
from src.ui.interface import Interface

if TYPE_CHECKING:
    from src.game.game import Game


class InterfaceManager:
    _interfaces: dict[InterfaceStatus, list[Interface]]
    _interface_list: list[Interface]
    _game: 'Game'
    _current_status: InterfaceStatus | None
    _status_history: list[InterfaceStatus]

    def __init__(self, game: 'Game') -> None:
        """
        Initialize the instance.

        Args:
            game: Game instance associated with the component.
        """
        self._interfaces = {}
        self._interface_list = []
        self._game = game
        self._current_status = None
        self._status_history = []

    def set_interface(
                self,
                status: list[InterfaceStatus] | InterfaceStatus,
                interface: Interface
            ) -> None:
        """
        Assign the interface.

        Args:
            status: New state to assign to the object.
            interface: Interface used by the operation.
        """
        if isinstance(status, InterfaceStatus):
            self._interfaces.setdefault(status, []).append(interface)
            self._interface_list.append(interface)
        else:
            for _status in status:
                self.set_interface(_status, interface)
        interface.hide()

    def get_interfaces(self) -> list[Interface]:
        """
        Return the current interfaces.

        Returns:
            The current interfaces.
        """
        if self._current_status is None:
            return []
        return (self._interfaces.get(self._current_status) or [])[::-1]

    def get_status(self) -> InterfaceStatus | None:
        """
        Return the current status.

        Returns:
            The current status.
        """
        return self._current_status

    def set_status(
            self, status: InterfaceStatus, remember: bool = True
            ) -> None:
        """
        Assign the status.

        Args:
            status: New state to assign to the object.
            remember: Remember used by the operation.
        """
        if status == self._current_status:
            return
        if remember and self._current_status is not None:
            self._status_history.append(self._current_status)
        self._current_status = status
        self.refresh_interfaces()

    def back(self) -> bool:
        """
        Handle back.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        if not self._status_history:
            return False
        self._current_status = self._status_history.pop()
        self.refresh_interfaces()
        return True

    def refresh_interfaces(self) -> None:
        """
        Handle refresh interfaces.
        """
        status = self._current_status
        if status not in self._interfaces:
            return
        target_interfaces: list[Interface] = self._interfaces[status]
        for interface in self._interface_list:
            if (
                not interface.is_hidden()
                and interface not in target_interfaces
            ):
                interface.hide()
            elif interface in target_interfaces and interface.is_hidden():
                interface.display()
