from collections.abc import Callable

import pygame

from src.app import App
from src.core import Alive, Collider, Displayable, Edible, Entity, Level, Tile
from src.core.movable import Movable
from src.game.ameliorations import (
    AmeliorationStore,
    ExpSkill,
    SpeedSkill,
    SuperTimeSkill,
)
from src.game.ameliorations.amelioration import Amelioration
from src.game.characters.ghost_state import GhostState
from src.game.characters.player_state import PlayerState
from src.graphics import ImageTexture
from src.graphics.super_meshes import Bar
from src.utils import Direction, Pos


class Player(Alive, Collider, Movable, Displayable, Entity):
    _inverse_mesh_by_direction: dict[ImageTexture, Direction | None]
    _mesh_by_direction: dict[Direction | None, ImageTexture]
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
    _super_time: float
    _cheat: bool

    def __init__(
                self,
                id: str,
                tile: Pos | Tile,
                level: Level,
                level_exp_multiplier: float,
                first_level_exp: float,
                exp_per_second: float,
                app: App
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

        self.cheat = True
        self._ameliorations = AmeliorationStore()
        self._level_exp_multiplier = level_exp_multiplier
        self._next_level_exp = first_level_exp
        self._exp_per_second = exp_per_second
        self._level_bar = None
        self._actual_level = 0
        self._exp_points = 0
        self._level_exp = 0
        self.set_state(PlayerState.NORMAL)

    def add_amelioration(self, amelioration: Amelioration) -> None:
        self._ameliorations.add(amelioration)

    def get_speed(self) -> float:
        initial_speed: float = super().get_speed()
        multiplier: float = sum([
            s.get_skill(SpeedSkill).get_value()
            for s in self._ameliorations.gets(SpeedSkill)
        ])

        return initial_speed + initial_speed * multiplier / 100

    def get_super_time(self) -> float:
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

    def init_mesh(self) -> None:
        self._mesh_by_direction = {
            Direction.NORTH: ImageTexture.create_blank(
                    "assets/characters/pacman/north_0.png"
                ),
            Direction.EAST: ImageTexture.create_blank(
                    "assets/characters/pacman/east_0.png"
                ),
            Direction.SOUTH: ImageTexture.create_blank(
                    "assets/characters/pacman/south_0.png"
                ),
            Direction.WEST: ImageTexture.create_blank(
                    "assets/characters/pacman/west_0.png"
                ),
            None: ImageTexture.create_blank(
                    "assets/characters/pacman/west_full.png"
                )
        }

        self._inverse_mesh_by_direction = {
            mesh: direction
            for direction, mesh in self._mesh_by_direction.items()
        }

        self._mesh = self._mesh_by_direction[None]

    def get_texture(self) -> ImageTexture:
        return self._mesh_by_direction[self._direction]

    def try_move(self, direction: Direction) -> bool:
        same = direction == self._direction
        if super().try_move(direction):
            if not same:
                self.update_mesh()
            return True
        return False

    def update(self, dt: float) -> None:
        super().update(dt)

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

    def update_mesh(self) -> None:
        actual_texture = self._mesh.texture
        actual_mesh = self._mesh_by_direction[
                self._inverse_mesh_by_direction[self._mesh]
            ]
        if not actual_mesh.texture:
            actual_mesh.texture = actual_texture

        return super().update_mesh()

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
            self.refresh_level_text()
            self.set_bar_goal()

    def set_super_state(self, time: float) -> None:
        self.set_state(PlayerState.SUPER)
        self._super_time = time + self.get_super_time()

    def on_death(self) -> None:
        self._direction = None
        super().on_death()
