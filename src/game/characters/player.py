from collections.abc import Callable
from random import sample
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.game.game import Game

import pygame

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
    _cheat: bool
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

        self._cheat = False
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

    def add_amelioration(self, amelioration: Amelioration) -> None:
        self._ameliorations.add(amelioration)

    def get_luck(self) -> float:
        multiplier: float = sum([
            s.get_skill(LuckSkill).get_value()
            for s in self._ameliorations.gets(LuckSkill)
        ])

        return 1 + 1 * multiplier / 100

    def get_speed(self) -> float:
        initial_speed: float = super().get_speed()
        multiplier: float = sum([
            s.get_skill(SpeedSkill).get_value()
            for s in self._ameliorations.gets(SpeedSkill)
        ])

        return initial_speed + initial_speed * multiplier / 100

    def get_upgrade_power(self) -> float:
        return sum(
            skill.get_value()
            for skill in (
                amelioration.get_skill(PowerSkill)
                for amelioration in self._ameliorations.gets(PowerSkill)
            )
        )

    def get_additional_super_time(self) -> float:
        return sum(
            [s.get_skill(SuperTimeSkill).get_value()
             for s in self._ameliorations.gets(SuperTimeSkill)]
        )

    def set_state(self, state: PlayerState) -> None:
        self._state = state

    def get_state(self) -> PlayerState:
        return self._state

    def on_collision(self, other: 'Collider') -> None:
        from src.game.characters import Ghost
        if not isinstance(other, Entity):
            return

        if isinstance(other, Edible):
            other.eat(self)

        if isinstance(other, Ghost):
            match other.get_state():
                case GhostState.CHASE:
                    self.set_health(0)
                case GhostState.FRIGHTENED:
                    other.set_state(GhostState.EATEN)

        super().on_collision(other)

    def on_collision_exit(self, other: 'Collider') -> None:
        super().on_collision_exit(other)

    def try_move(self, direction: Direction) -> bool:
        # same = direction == self._direction
        if super().try_move(direction):
            # if not same:
            #     self.update_mesh()
            return True
        return False

    def update(self, dt: float) -> None:
        super().update(dt)
        self.update_animation(dt)

        self.add_exp(dt * self._exp_per_second)

        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.try_move(Direction.NORTH)
        if keys[pygame.K_DOWN]:
            self.try_move(Direction.SOUTH)
        if keys[pygame.K_LEFT]:
            self.try_move(Direction.WEST)
        if keys[pygame.K_RIGHT]:
            self.try_move(Direction.EAST)

    def on_arrive(self, tile: Tile, direction: Direction) -> None:
        if self._queued is not None:
            if not self.try_move(self._queued):
                self.try_move_forward()
            else:
                self._queued = None
        else:
            self.try_move_forward()

        return super().on_arrive(tile, direction)

    def refresh_bar_progression(self) -> None:
        if not self._level_bar:
            return
        self._level_bar.set_progression(
                self._exp_points - self._level_exp
            )

    def refresh_level_text(self) -> None:
        self.set_level_text(self._actual_level)

    def set_bar_goal(self) -> None:
        if not self._level_bar:
            return
        self._level_bar.set_goal(
                self._next_level_exp - self._level_exp
            )

    def add_exp(self, amount: float) -> None:
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
        self._direction = None
        super().on_death()

    def init_displayable(self) -> None:
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
        return self._animations[self._direction]

    def on_level_up(self) -> None:
        self._game._amelioration_interface.start()

    def get_next_ameliorations(self) -> tuple[
                type[Amelioration], ...
            ]:
        ameliorations = Amelioration.__subclasses__()
        return tuple(sample(ameliorations, min(3, len(ameliorations))))
