from collections.abc import Callable
from random import sample
from typing import TYPE_CHECKING

from src.settings.action_key import ActionKey

if TYPE_CHECKING:
    from src.game.game import Game

from src.app import App
from src.core import Alive, Collider, Displayable, Edible, Entity, Level, Tile
from src.core.movable import Movable
from src.game.ameliorations import (
    AmeliorationStore,
    ExpSkill,
    LuckSkill,
    PowerSkill,
    SpeedSkill,
    SuperTimeSkill,
)
from src.game.ameliorations.amelioration import Amelioration
from src.game.characters.ghost_state import GhostState
from src.game.characters.player_state import PlayerState
from src.game.game_status import GameStatus
from src.graphics.super_meshes import Bar
from src.texture.animation_player import AnimationPlayer
from src.texture.texture_keys import TextureKeys
from src.utils import Direction, Pos


class Player(Alive, Collider, Movable, Displayable, Entity):
    _animations: dict[Direction | None, AnimationPlayer]

    set_level_text: Callable[[int], None]
    _ameliorations: AmeliorationStore
    _level_exp_multiplier: float
    _next_level_exp: float
    _exp_per_second: float
    _level_bar: Bar | None
    _state: PlayerState
    _actual_level: int
    _exp_points: float
    _level_exp: float
    _wallhack: bool
    _godmod: bool
    _noclip: bool
    _game: 'Game'

    def __init__(
                self,
                id: str,
                tile: Pos | Tile,
                level: Level,
                level_exp_multiplier: float,
                first_level_exp: float,
                exp_per_second: float,
                app: App,
                game: 'Game'
            ) -> None:
        """
        Initialize the instance.

        Args:
            id: Identifier assigned to the object.
            tile: Grid tile occupied by or assigned to the entity.
            level: Level containing the entity or navigation data.
            level_exp_multiplier: Level exp multiplier used by the operation.
            first_level_exp: First level exp used by the operation.
            exp_per_second: Exp per second used by the operation.
            app: Application instance that owns the object.
            game: Game instance associated with the component.
        """
        super().__init__(
            name=id,
            tile=tile,
            level=level,
            solid=True,
            radius=0.45,
            speed=6,
            proportion=0.9,
            primary=True,
            lives=3,
            app=app
        )

        self._ameliorations = AmeliorationStore()
        self._level_exp_multiplier = level_exp_multiplier
        self._next_level_exp = first_level_exp
        self._exp_per_second = exp_per_second
        self._level_bar = None
        self._actual_level = 0
        self._exp_points = 0
        self._level_exp = 0
        self._game = game
        self.set_state(PlayerState.NORMAL)

        self._wallhack = False
        self._godmod = False
        self._noclip = False

    def add_amelioration(self, amelioration: Amelioration) -> None:
        """
        Add the amelioration to the collection.

        Args:
            amelioration: Amelioration used by the operation.
        """
        if type(amelioration) not in [
                    a.__class__ for a in self._ameliorations.all()
                ]:
            self._ameliorations.add(amelioration)
        self._game._stats_interface.refresh_ameliorations()

    def get_luck(self) -> float:
        """
        Return the current luck.

        Returns:
            The current luck.
        """
        multiplier: float = sum([
            s.get_skill(LuckSkill).get_value()
            for s in self._ameliorations.gets(LuckSkill)
        ])

        return 1 + 1 * multiplier / 100

    def get_speed(self) -> float:
        """
        Return the current speed.

        Returns:
            The current speed.
        """
        initial_speed: float = super().get_speed()
        multiplier: float = sum([
            s.get_skill(SpeedSkill).get_value()
            for s in self._ameliorations.gets(SpeedSkill)
        ])

        return initial_speed + initial_speed * multiplier / 100

    def get_upgrade_power(self) -> float:
        """
        Return the current upgrade power.

        Returns:
            The current upgrade power.
        """
        return sum(
            skill.get_value()
            for skill in (
                amelioration.get_skill(PowerSkill)
                for amelioration in self._ameliorations.gets(PowerSkill)
            )
        )

    def get_additional_super_time(self) -> float:
        """
        Return the current additional super time.

        Returns:
            The current additional super time.
        """
        return sum(
            [s.get_skill(SuperTimeSkill).get_value()
             for s in self._ameliorations.gets(SuperTimeSkill)]
        )

    def set_state(self, state: PlayerState) -> None:
        """
        Assign the state.

        Args:
            state: State used by the operation.
        """
        self._state = state

    def get_state(self) -> PlayerState:
        """
        Return the current state.

        Returns:
            The current state.
        """
        return self._state

    def on_collision(self, other: 'Collider') -> None:
        """
        Handle the collision event.

        Args:
            other: Other collider involved in the collision.
        """
        from src.game.characters import Ghost
        if not isinstance(other, Entity):
            return

        if isinstance(other, Edible) and other.eat(self):
            self._game.record_collection(
                other.get_reward(),
                ghost=isinstance(other, Ghost),
            )

        if isinstance(other, Ghost):
            match other.get_state():
                case GhostState.CHASE:
                    if not self._godmod:
                        self.set_health(0)
                case GhostState.FRIGHTENED:
                    other.set_state(GhostState.EATEN)

        super().on_collision(other)

    def on_collision_exit(self, other: 'Collider') -> None:
        """
        Handle the collision exit event.

        Args:
            other: Other collider involved in the collision.
        """
        super().on_collision_exit(other)

    def try_move(self, direction: Direction, force: bool = False) -> bool:
        """
        Handle try move.

        Args:
            direction: Direction in which the entity should move.
            force: Whether to bypass the usual movement restrictions.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        if self._game.get_status() == GameStatus.INITIALIZING:
            self._game.set_status(GameStatus.RUNNING)
        return super().try_move(direction, self._noclip or force)

    def try_move_forward(self, force: bool = False) -> bool:
        """
        Handle try move forward.

        Args:
            force: Whether to bypass the usual movement restrictions.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        return super().try_move_forward(self._noclip or force)

    def update(self, dt: float) -> None:
        """
        Handle update.

        Args:
            dt: Elapsed time since the previous update, in seconds.
        """
        super().update(dt)
        self.update_animation(dt)

        self.add_exp(dt * self._exp_per_second)



    def handle_key(self, key: int) -> None:
        if self._game.get_status() not in [
                    GameStatus.RUNNING,
                    GameStatus.INITIALIZING
                ]:
            return

        if key in self.app.key_manager.get_keys(ActionKey.MOVE_UP):
            self.try_move(Direction.NORTH)
        if key in self.app.key_manager.get_keys(ActionKey.MOVE_DOWN):
            self.try_move(Direction.SOUTH)
        if key in self.app.key_manager.get_keys(ActionKey.MOVE_LEFT):
            self.try_move(Direction.WEST)
        if key in self.app.key_manager.get_keys(ActionKey.MOVE_RIGHT):
            self.try_move(Direction.EAST)

    def on_arrive(self, tile: Tile, direction: Direction) -> None:
        """
        Handle the arrive event.

        Args:
            tile: Grid tile occupied by or assigned to the entity.
            direction: Direction in which the entity should move.
        """
        if self._queued is not None:
            if not self.try_move(self._queued):
                self.try_move_forward()
            else:
                self._queued = None
        else:
            self.try_move_forward()

        return super().on_arrive(tile, direction)

    def refresh_bar_progression(self) -> None:
        """
        Handle refresh bar progression.
        """
        if not self._level_bar:
            return
        self._level_bar.set_progression(
                self._exp_points - self._level_exp
            )

    def refresh_level_text(self) -> None:
        """
        Handle refresh level text.
        """
        self.set_level_text(self._actual_level)

    def set_bar_goal(self) -> None:
        """
        Assign the bar goal.
        """
        if not self._level_bar:
            return
        self._level_bar.set_goal(
                self._next_level_exp - self._level_exp
            )

    def add_exp(self, amount: float) -> None:
        """
        Add the exp to the collection.

        Args:
            amount: Amount used by the operation.
        """
        multiplier: float = sum(
            [s.get_skill(ExpSkill).get_value()
             for s in self._ameliorations.gets(ExpSkill)]
        )
        self._exp_points += amount + amount * multiplier / 100
        self.refresh_bar_progression()
        if self._exp_points >= self._next_level_exp:
            temp = self._next_level_exp
            self._next_level_exp += (
                    self._next_level_exp - self._level_exp
                ) * self._level_exp_multiplier
            self._level_exp = temp
            self._actual_level += 1
            self.on_level_up()
            self.refresh_level_text()
            self.set_bar_goal()

    def on_death(self) -> None:
        """
        Handle the death event.
        """
        self._direction = None
        if self._godmod:
            return
        super().on_death()

    def init_displayable(self) -> None:
        """
        Initialize the associated state.
        """
        self._animations = {
            direction: AnimationPlayer(
                self.app.texture.get(TextureKeys.PACMAN, direction.to_string())
            )
            for direction in Direction
        }
        self._animations[None] = AnimationPlayer(self.app.texture.get(
            TextureKeys.PACMAN,
            'static'
        ))

    def get_animation(self) -> AnimationPlayer:
        """
        Return the current animation.

        Returns:
            The current animation.
        """
        return self._animations[self._direction]

    def on_level_up(self) -> None:
        """
        Handle the level up event.
        """
        self._game._amelioration_interface.start()

    def get_next_ameliorations(self) -> tuple[
                Amelioration, ...
            ]:
        """
        Return the current next ameliorations.

        Returns:
            The current next ameliorations.
        """
        current_ameliorations = self._ameliorations.all()

        if len(current_ameliorations) ==\
                self._game._config.max_player_ameliorations:
            return tuple(sample(
                current_ameliorations + current_ameliorations, 3
            ))

        ameliorations = Amelioration.__subclasses__()
        return tuple(
            [
                self._ameliorations.get_by_type(a) or a() for a in sample(
                    ameliorations, min(3, len(ameliorations))
                )
            ]
        )
