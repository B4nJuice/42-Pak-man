from typing import TYPE_CHECKING, cast

from src.core.displayable import DisplayableEntity
from src.texture.animation_player import AnimationPlayer
from src.texture.texture_keys import TextureKeys

if TYPE_CHECKING:
    from src.game.characters import Player

from src.app import App
from src.core import Collider, Displayable, Edible, Entity, Level, Tile
from src.utils import Pos


class SuperPacGum(Edible, Collider, Displayable, Entity):
    _animation: AnimationPlayer

    def __init__(
                self,
                id: str,
                pos: Pos | Tile,
                level: Level,
                reward: float,
                app: App
            ) -> None:
        super().__init__(
            name=id,
            tile=pos,
            level=level,
            solid=False,
            radius=0.15,
            proportion=0.3,
            reward=reward,
            app=app
        )

    def on_collision(self, other: 'Collider') -> None:
        if not isinstance(other, Entity):
            return

        return super().on_collision(other)

    def eat(self, eater: 'Player') -> bool:
        if super().eat(eater):
            self.level.unregister_entity(cast(DisplayableEntity, self))
            self.level.state.set_frightened_phase()
            return True
        return False

    def init_displayable(self) -> None:
        self._animation = AnimationPlayer(
            self.app.texture.get(TextureKeys.SUPER_PACGUM)
        )

    def get_animation(self) -> AnimationPlayer:
        return self._animation
