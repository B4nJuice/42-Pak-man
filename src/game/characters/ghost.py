from abc import abstractmethod

from src.app import App
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
from src.game.characters.ghost_type import GhostType
from src.graphics import Color
from src.texture.animation_player import AnimationPlayer
from src.texture.texture_keys import TextureKeys
from src.utils import Direction, Pos


class Ghost(Collider, AI, Movable, Edible, Displayable, Entity):
    _state: GhostState
    _state_cooldown: float | None
    a_star: AStar
    _texture_path: str
    _spawn_tile: Tile
    _frightened_tile: Tile | None
    _base_speed: float
    _dead_speed: float
    _path_color: Color

    _ghost_type: GhostType
    _texture_key: TextureKeys

    _animations_alive: dict[Direction, AnimationPlayer]
    _animations_eaten: dict[Direction, AnimationPlayer]
    _animation_frightened: AnimationPlayer

    def __init__(
                self, name: str,
                tile: Pos | Tile,
                level: Level,
                reward: float,
                app: App,
                ghost_type: GhostType,
                texture_key: TextureKeys,
                update_tracking_interval: float | None = 0.6,
                path_color: Color = Color(255, 0, 0, 100),
            ) -> None:
        """
        Initialize the instance.

        Args:
            name: Name assigned to the object or requested value.
            tile: Grid tile occupied by or assigned to the entity.
            level: Level containing the entity or navigation data.
            reward: Reward used by the operation.
            app: Application instance that owns the object.
            ghost_type: Ghost type used by the operation.
            texture_key: Texture key used by the operation.
            update_tracking_interval: Update tracking interval used by
            the operation.
            path_color: Path color used by the operation.
        """
        self._ghost_type = ghost_type
        self._texture_key = texture_key

        super().__init__(
            name=name,
            tile=tile,
            level=level,
            solid=True,
            proportion=0.9,
            reward=reward,
            edible=False,
            update_tracking_interval=update_tracking_interval,
            app=app
        )
        self._base_speed = 4.0
        self._dead_speed = 10.0

        self._path_color = path_color
        self.a_star = AStar(level)
        self.set_state(GhostState.CHASE)
        self.set_spawn_tile(self.get_tile())
        self._state_cooldown = -1
        self._frightened_tile = None

    def get_state(self) -> GhostState:
        """
        Return the current state.

        Returns:
            The current state.
        """
        return self._state

    def is_edible(self) -> bool:
        """
        Check whether the edible condition holds.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        return self._state == GhostState.FRIGHTENED

    def set_state(self, state: GhostState) -> None:
        """
        Assign the state.

        Args:
            state: State used by the operation.
        """
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
        """
        Handle the arrive ai event.
        """
        match self._state:
            case GhostState.FRIGHTENED:
                self._frightened_tile = None
            case GhostState.EATEN:
                self.set_state(GhostState.WAITING_RESPAWN)

        return super().on_arrive_ai()

    def get_spawn_tile(self) -> Tile:
        """
        Return the current spawn tile.

        Returns:
            The current spawn tile.
        """
        return self._spawn_tile

    def set_spawn_tile(self, tile: Tile) -> None:
        """
        Assign the spawn tile.

        Args:
            tile: Grid tile occupied by or assigned to the entity.
        """
        self._spawn_tile = tile

    @abstractmethod
    def get_chase_tracking_tile(self) -> Tile:
        """
        Return the current chase tracking tile.

        Returns:
            The current chase tracking tile.
        """
        pass

    def get_frightened_tracking_tile(self) -> Tile:
        """
        Return the current frightened tracking tile.

        Returns:
            The current frightened tracking tile.
        """
        if self._frightened_tile is None:
            self._frightened_tile = self.generate_new_frightened_tile()

        return self._frightened_tile

    def generate_new_frightened_tile(self) -> Tile:
        """
        Handle generate new frightened tile.

        Returns:
            The value produced by the generate new frightened tile operation.
        """
        return self.level.get_random_valid_tile()

    def get_tracking_tile(self) -> Tile:
        """
        Return the current tracking tile.

        Returns:
            The current tracking tile.
        """
        match self.get_state():
            case GhostState.CHASE:
                return self.get_chase_tracking_tile()
            case GhostState.EATEN | GhostState.WAITING_RESPAWN:
                return self.get_spawn_tile()
            case GhostState.FRIGHTENED:
                return self.get_frightened_tracking_tile()

    def on_collision(self, other: 'Collider') -> None:
        """
        Handle the collision event.

        Args:
            other: Other collider involved in the collision.
        """
        if not isinstance(other, Entity):
            return

        super().on_collision(other)

    def go_to(self, tile: Tile) -> None:
        """
        Handle go to.

        Args:
            tile: Grid tile occupied by or assigned to the entity.
        """
        if tile == self.get_tile() and self.is_moving():
            self.clear_next_moves()
            self.on_arrive_ai()
            return

        path = self.a_star.find_path(
            start=self.get_target_tile(),
            end=tile
        )

        self.clear_next_moves()
        self.apply_path(path)

    def update(self, dt: float) -> None:
        """
        Handle update.

        Args:
            dt: Elapsed time since the previous update, in seconds.
        """
        super().update(dt)

        if not self._freeze:
            self.update_ai(dt)

        self.update_animation(dt)
        self.update_state(dt)

    def update_state(self, dt: float) -> None:
        """
        Update the state.

        Args:
            dt: Elapsed time since the previous update, in seconds.
        """
        if self._state_cooldown is None:
            return

        self._state_cooldown -= dt
        if self._state_cooldown <= 0:
            if self.level.state.frightened_phase.is_active():
                self.set_state(GhostState.FRIGHTENED)
            else:
                self.set_state(GhostState.CHASE)

    def init_displayable(self) -> None:
        """
        Initialize the associated state.
        """
        self._animations_alive = {
            direction: AnimationPlayer(
                self.app.texture.get(self._texture_key, direction.to_string())
            )
            for direction in Direction
        }
        self._animations_eaten = {
            direction: AnimationPlayer(self.app.texture.get(
                TextureKeys.GHOST_EATEN,
                direction.to_string()
            ))
            for direction in Direction
        }
        self._animation_frightened = AnimationPlayer(
            self.app.texture.get(TextureKeys.GHOST_FRIGHTENED)
        )

    def get_animation(self) -> AnimationPlayer:
        """
        Return the current animation.

        Returns:
            The current animation.
        """
        match self.get_state():
            case GhostState.CHASE | GhostState.WAITING_RESPAWN:
                if self._direction is None:
                    return self._animations_alive[Direction.EAST]
                return self._animations_alive[self._direction]
            case GhostState.EATEN:
                if self._direction is None:
                    return self._animations_eaten[Direction.EAST]

                return self._animations_eaten[self._direction]
            case GhostState.FRIGHTENED:
                return self._animation_frightened

    def update_tracking(self) -> None:
        """
        Update the tracking.
        """
        if self._tracking_tile is None:
            return

        self.go_to(self._tracking_tile)
        super().update_tracking()
