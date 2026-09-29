from src.graphics import MeshLayer, Position, Color
from src.graphics.super_meshes import Rectangle
from src.ui import Interface
from src.game import Game


class StatsInterface(Interface):
    def __init__(self, game : Game) -> None:
        self.game: Game = game
        self.layer: MeshLayer = MeshLayer()

        self.x_offset: int = round(self.game._config.screen_width * 0.02)
        self.y_offset: int = round(self.game._config.screen_height * 0.02)
        self.width: int = round(self.game._config.screen_width * 0.25) - self.x_offset
        self.height: int = self.game._config.screen_height - self.y_offset

        self.border: Rectangle = Rectangle(
            Color(*self.game._config.stats_border_color),
            Position(self.x_offset, self.y_offset),
            self.width - self.x_offset,
            self.height - self.y_offset,
            3,
            is_dynamic=True,
            smooth_end=True
        )

        self.layer.meshes.append(self.border)

    def get_layer(self) -> MeshLayer:
        return self.layer
