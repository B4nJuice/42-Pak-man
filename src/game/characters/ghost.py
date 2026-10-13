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
from src.graphics import ImageTexture
from src.utils import Direction, Pos


class Ghost(Collider, AI, Movable, Edible, Displayable, Entity):
    _state: GhostState
    _state_cooldown: float | None
    a_star: AStar
    _texture_path: str
    _meshs: dict[Direction, list[ImageTexture]]
    _spawn_tile: Tile
    _frightened_tile: Tile | None
    _base_speed: float
    _dead_speed: float

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
        self._base_speed = 4.0
        self._dead_speed = 10.0

        self.a_star = AStar(level)
        self.set_state(GhostState.CHASE)
        self.set_spawn_tile(self.get_tile())
        self._state_cooldown = -1
        self._frightened_tile = None

    def get_state(self) -> GhostState:
        return self._state

    def is_edible(self) -> bool:
        return self._state == GhostState.FRIGHTENED

    def set_state(self, state: GhostState) -> None:
        self._state_cooldown = None
        self.set_edible(False)

        match state:
            case GhostState.CHASE:
                self.set_speed(self._base_speed)
            case GhostState.FRIGHTENED:
                self.set_edible(True)
                self.set_speed(self._base_speed)
            case GhostState.EATEN:
                self.set_speed(self._dead_speed)
            case GhostState.WAITING_RESPAWN:
                self._state_cooldown = 2.0

        self._state = state
        self.force_update_tracking()

    def on_arrive_ai(self) -> None:
        match self._state:
            case GhostState.FRIGHTENED:
                self._frightened_tile = None
            case GhostState.EATEN:
                self.set_state(GhostState.WAITING_RESPAWN)

        return super().on_arrive_ai()

    def get_spawn_tile(self) -> Tile:
        return self._spawn_tile

    def set_spawn_tile(self, tile: Tile) -> None:
        self._spawn_tile = tile

    @abstractmethod
    def get_chase_tracking_tile(self) -> Tile:
        pass

    def get_frightened_tracking_tile(self) -> Tile:
        if self._frightened_tile is None:
            self._frightened_tile = self.generate_new_frightened_tile()

        return self._frightened_tile

    def generate_new_frightened_tile(self) -> Tile:
        return self.level.get_random_valid_tile()

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

    def update(self, dt: float) -> None:
        super().update(dt)
        self.update_ai(dt)
        self.update_mesh()

        self.update_state(dt)

    def update_state(self, dt: float) -> None:
        if self._state_cooldown is None:
            return

        self._state_cooldown -= dt
        if self._state_cooldown <= 0:
            if self.level.state.frightened_phase.is_active():
                self.set_state(GhostState.FRIGHTENED)
            else:
                self.set_state(GhostState.CHASE)

    def get_mesh(self) -> ImageTexture:
        if not self._direction:
            return self._meshs[Direction.EAST][0]

        return self._meshs[self._direction][0]

    def get_texture(self) -> ImageTexture:
        if self._direction is None:
            return self._meshs[Direction.EAST][0]

        return self._meshs[self._direction][0]

    def update_tracking(self) -> None:
        if self._tracking_tile is None:
            return

        self.go_to(self._tracking_tile)
        super().update_tracking()
