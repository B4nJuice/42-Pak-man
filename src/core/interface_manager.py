from src.game.game import Game
from src.game.game_status import GameStatus
from src.ui.interface import Interface


class InterfaceManager:
    _interfaces: dict[GameStatus, Interface]
    _game: Game

    def __init__(self, game: Game) -> None:
        self._interfaces = {}
        self._game = game

    def set_interface(
                self,
                status: list[GameStatus] | GameStatus,
                interface: Interface
            ) -> None:
        if isinstance(status, GameStatus):
            self._interfaces[status] = interface
        else:
            for _status in status:
                self.set_interface(_status, interface)

    def refresh_interfaces(self) -> None:
        status: GameStatus = self._game.get_status()
        target_interface: Interface = self._interfaces[status]
        for interface in self._interfaces.values():
            if not interface.is_hidden() and interface != target_interface:
                interface.hide()
            elif interface == target_interface and interface.is_hidden():
                interface.display()
