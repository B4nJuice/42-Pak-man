from typing import TYPE_CHECKING

from src.game.game_status import GameStatus
from src.ui.interface import Interface

if TYPE_CHECKING:
    from src.game.game import Game


class InterfaceManager:
    _interfaces: dict[GameStatus, list[Interface]]
    _interface_list: list[Interface]
    _game: 'Game'

    def __init__(self, game: 'Game') -> None:
        self._interfaces = {}
        self._interface_list = []
        self._game = game

    def set_interface(
                self,
                status: list[GameStatus] | GameStatus,
                interface: Interface
            ) -> None:
        if isinstance(status, GameStatus):
            self._interfaces.setdefault(status, []).append(interface)
            self._interface_list.append(interface)
        else:
            for _status in status:
                self.set_interface(_status, interface)

    def get_interfaces(self) -> list[Interface]:
        return self._interfaces.get(self._game.get_status()) or []

    def refresh_interfaces(self) -> None:
        status: GameStatus = self._game.get_status()
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
