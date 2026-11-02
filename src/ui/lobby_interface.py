from typing import TYPE_CHECKING

from src.graphics import Position
from src.texture.texture_keys import TextureKeys

if TYPE_CHECKING:
    from src.game.game import Game

from src.core.displayable import SimpleDisplayable
from src.graphics.mesh_layer import MeshLayer
from src.ui.interface import Interface


class LobbyInterface(Interface):
    game: 'Game'
    layer: MeshLayer

    def __init__(self, game: 'Game') -> None:
        super().__init__(game)
        self.game = game
        self.layer = MeshLayer()

        screen_width = self.game._screen.width
        screen_height = self.game._screen.height
        config = self.game._config
        size = self.game._app.size
        fonts = self.game._app.fonts

        self.layer.meshes.append(SimpleDisplayable(
            app=game._app,
            texture_key=TextureKeys.MAIN_BACKDROP.str(),
            position=Position(screen_width // 2, screen_height // 2),
            width=screen_width,
            height=screen_height
        ))


    def get_layer(self) -> MeshLayer:
        return self.layer
