import pygame

from src.core import Collider, Displayable, Entity, Level, Tile
from src.core.movable import Movable
from src.graphics import ImageTexture, OperationEnum, Position
from src.utils import Direction, Pos


class Player(Collider, Movable, Displayable, Entity):
    def __init__(self, id: str, tile: Pos | Tile, level: Level):
        super().__init__(
            name=id,
            tile=tile,
            level=level,
            solid=True,
            radius=0.45,
            speed=1,
            proportion=0.9
        )

    def on_collision(self, other: 'Collider') -> None:
        super().on_collision(other)
        if not isinstance(other, Entity):
            return

        print(f'Collision with {other.get_name()!r}')

    def on_collision_exit(self, other: 'Collider') -> None:
        super().on_collision_exit(other)

    def init_mesh(self) -> None:
        self._mesh = ImageTexture(
            path='assets/characters/pacman/d0_0.png',
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

        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.try_move(Direction.NORTH)
        if keys[pygame.K_DOWN]:
            self.try_move(Direction.SOUTH)
        if keys[pygame.K_LEFT]:
            self.try_move(Direction.WEST)
        if keys[pygame.K_RIGHT]:
            self.try_move(Direction.WEST)

    def on_arrive(self, tile: Tile) -> None:
        print(f'Arrived at {tile.get_pos()}')

        return super().on_arrive(tile)

    def update_mesh(self) -> None:
        return super().update_mesh()
