from bisect import bisect_right
import pygame


from src.graphics.super_meshes import Bar
from src.core import Collider, Displayable, Entity, Level, Tile
from src.core.movable import Movable
from src.graphics import ImageTexture, OperationEnum, Position
from src.utils import Direction, Pos


class Player(Collider, Movable, Displayable, Entity):
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
        self._mesh = ImageTexture(
            path='assets/characters/ghosts/red/east_0.png',
            position=Position(0, 0),
            width=0,
            height=0,
            operation=OperationEnum.SET,
            is_dynamic=False,
        )

    def try_move(self, direction: Direction) -> bool:
        if super().try_move(direction):
            print(f'Moving to {direction}')
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

    def on_arrive(self, tile: Tile, direction: Direction) -> None:
        print(f'Arrived at {tile.get_pos()}')
        if self._queued is not None:
            self.try_move(self._queued)
            self._queued = None
        else:
            self.try_move(direction)

        return super().on_arrive(tile, direction)

    def update_mesh(self) -> None:
        return super().update_mesh()

    def refresh_bar_progression(self) -> None:
        if not self._level_bar:
            return
        self._level_bar.set_progression(
                self._exp_points - self._level_exp
            )

    def set_bar_goal(self) -> None:
        if not self._level_bar:
            return
        self._level_bar.goal(
                self._next_level_exp - self._level_exp
            )

    def add_exp(self, amount: int) -> None:
        self._exp_points += amount
        self.refresh_bar_progression()
        if self._exp_points >= self._next_level_exp:
            self._level_exp = self._next_level_exp
            self._next_level_exp +=\
                self._next_level_exp * self._level_exp_multiplier
            self._actual_level += 1
            self.set_bar_goal()
