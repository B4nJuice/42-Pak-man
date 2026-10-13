from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.level import Level


from .state_types import CooldownState, Updatable


class StateManager:
    level: 'Level'
    _to_update: list[Updatable]
    frightened_phase: CooldownState

    def __init__(self, level: 'Level') -> None:
        self.level = level
        self._to_update = []

        self.frightened_phase = CooldownState(default=10.0)
        self.frightened_phase.register_callback(self._set_ghost_to_chase)

        self._to_update.append(self.frightened_phase)

    def set_to_default(self) -> None:
        self.frightened_phase.set(0.0)

    def set_frightened_phase(self) -> None:
        from src.game.characters.ghost import Ghost
        from src.game.characters.ghost_state import GhostState
        from src.game.characters.player import Player
        from src.game.characters.player_state import PlayerState

        self.frightened_phase.set_default()

        for ghost in self.level.store.gets(Ghost):
            ghost.set_state(GhostState.FRIGHTENED)
        self.level.store.get(Player).set_state(PlayerState.SUPER)

    def _set_ghost_to_chase(self) -> None:
        from src.game.characters.ghost import Ghost
        from src.game.characters.ghost_state import GhostState
        from src.game.characters.player import Player
        from src.game.characters.player_state import PlayerState

        for ghost in self.level.store.gets(Ghost):
            if ghost.get_state() == GhostState.FRIGHTENED:
                ghost.set_state(GhostState.CHASE)

        self.level.store.get(Player).set_state(PlayerState.NORMAL)

    def update(self, dt: float) -> None:
       for element in self._to_update:
           element.update(dt)
