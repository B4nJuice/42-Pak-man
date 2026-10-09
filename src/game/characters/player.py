from collections.abc import Callable

import pygame

from src.core import Collider, Displayable, Entity, Level, Tile
from src.core.movable import Movable
from src.graphics import ImageTexture
from src.graphics.super_meshes import Bar
from src.utils import Direction, Pos


class Player(Collider, Movable, Displayable, Entity):
    _inverse_mesh_by_direction: dict[ImageTexture, Direction | None]
    _mesh_by_direction: dict[Direction | None, ImageTexture]
    set_level_text: Callable[[int], None]
    _level_exp_multiplier: float
    _next_level_exp: float
    _exp_per_second: float
    _level_bar: Bar | None
    _actual_level: int
    _exp_points: float
    _level_exp: float

    def __init__(
                self,
                id: str,
                tile: Pos | Tile,
                level: Level
            ) -> None:
        super().__init__(
            name=id,
            tile=tile,
            level=level,
            solid=True,
            radius=0.45,
            speed=6,
            proportion=0.9
        )

        # TODO link params to the config

        self._level_exp_multiplier = 1.1
        self._next_level_exp = 100
        self._exp_per_second = 0.5
        self._level_bar = None
        self._actual_level = 0
        self._exp_points = 0
        self._level_exp = 0

    def on_collision(self, other: 'Collider') -> None:
        super().on_collision(other)
        if not isinstance(other, Entity):
            return

        print(f'Collision with {other.get_name()!r}')

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
            print(f'Moving to {direction}')
            if not same:
                self.update_mesh()
            return True
        print(f'Cannot move to {direction}')
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
        print(f'Arrived at {tile.get_pos()}')
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
        # pass

    def set_bar_goal(self) -> None:
        if not self._level_bar:
            return
        self._level_bar.set_goal(
                self._next_level_exp - self._level_exp
            )

    def add_exp(self, amount: float) -> None:
        self._exp_points += amount
        self.refresh_bar_progression()
        if self._exp_points >= self._next_level_exp:
            temp = self._next_level_exp
            self._next_level_exp +=\
                (self._next_level_exp - self._level_exp) * self._level_exp_multiplier
            self._level_exp = temp
            self._actual_level += 1
            self.refresh_level_text()
            self.set_bar_goal()
