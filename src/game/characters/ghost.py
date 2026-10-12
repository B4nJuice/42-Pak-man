from abc import abstractmethod
from pathlib import Path

from src.core import (
    AI,
    AStar,
    Collider,
    Displayable,
    Edible,
    Entity,
    Level,
    Tile,
)
from src.core.movable import Movable
from src.game.characters.ghost_state import GhostState
from src.game.characters.player import Player
from src.game.characters.player_state import PlayerState
from src.graphics import ImageTexture
from src.utils import Direction, Pos


class Ghost(Edible, Collider, AI, Movable, Displayable, Entity):
    _state: GhostState
    _state_cooldown: float | None
    a_star: AStar
    _texture_path: str
    _meshs: dict[Direction, list[ImageTexture]]
    _spawn_tile: Tile

    def __init__(
                self, name: str,
                tile: Pos | Tile,
                level: Level,
                reward: float,
                update_tracking_interval: float | None = 0.6,
            ) -> None:
        super().__init__(
            name=name,
            tile=tile,
            level=level,
            solid=True,
            proportion=0.9,
            reward=reward,
            edible=False,
            update_tracking_interval=update_tracking_interval
        )

        self.a_star = AStar(level)
        self.set_state(GhostState.CHASE)
        self.set_spawn_tile(self.get_tile())
        self._state_cooldown = -1

    def get_state(self) -> GhostState:
        return self._state

    def set_state(self, state: GhostState) -> None:
        match state:
            case GhostState.CHASE | GhostState.EATEN | GhostState.FRIGHTENED:
                self._state_cooldown = None
            case GhostState.WAITING_RESPAWN:
                self._state_cooldown = 2.0
        self._state = state

    def get_spawn_tile(self) -> Tile:
        return self._spawn_tile

    def set_spawn_tile(self, tile: Tile) -> None:
        self._spawn_tile = tile

    @abstractmethod
    def get_chase_tracking_tile(self) -> Tile:
        pass

    @abstractmethod
    def get_frightened_tracking_tile(self) -> Tile:
        pass

    def get_tracking_tile(self) -> Tile:
        match self.get_state():
            case GhostState.CHASE:
                return self.get_chase_tracking_tile()
            case GhostState.EATEN | GhostState.WAITING_RESPAWN:
                return self.get_spawn_tile()
            case GhostState.FRIGHTENED:
                return self.get_frightened_tracking_tile()

    def init_mesh(self) -> None:
        self._meshs = {
            direction: [
                ImageTexture.create_blank(Path(
                    self._texture_path, f'{direction.to_string()}_{i}.png'
                ).as_posix())
                for i in range(1)
            ]
            for direction in Direction
        }

    def on_collision(self, other: 'Collider') -> None:
        if not isinstance(other, Entity):
            return

        super().on_collision(other)

        self._mesh = self._meshs[Direction.EAST][0]

    def go_to(self, tile: Tile) -> None:
        path = self.a_star.find_path(
            start=self.get_target_tile(),
            end=tile
        )

        self.clear_next_moves()
        self.apply_path(path)

    def eat(self, eater: 'Player') -> bool:
        if eater.get_state() == PlayerState.SUPER:
            self.set_edible(True)

        return_state: bool = super().eat(eater)
        self.set_edible(False)
        return return_state

    def update(self, dt: float) -> None:
        super().update(dt)
        self.update_ai(dt)
        self.update_mesh()

    def update_state(self, dt: float) -> None:
        if self._state_cooldown is None:
            return

        self._state_cooldown -= dt
        if self._state_cooldown <= 0:
            self.set_state(GhostState.CHASE)

    def get_mesh(self) -> ImageTexture:
        if not self._direction:
            return self._meshs[Direction.EAST][0]

        return self._meshs[self._direction][0]

    def get_texture(self) -> ImageTexture:
        if self._direction is None:
            return self._meshs[Direction.EAST][0]

        return self._meshs[self._direction][0]
