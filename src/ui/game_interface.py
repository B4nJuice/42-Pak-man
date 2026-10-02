from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.game import Game
from src.graphics import Color, Position
from src.graphics.mesh_layer import MeshLayer
from src.graphics.super_meshes import AlignEnum, Bar, FontSequence, MeshLevel

from .interface import Interface


class GameInterface(Interface):
    def __init__(self, game: 'Game') -> None:
        self.game: Game = game
        self.layer: MeshLayer = MeshLayer()

        self.x_offset: int = round(self.game._config.screen_width * 0.25)
        self.y_offset: int = round(self.game._config.screen_height * 0.02)
        self.width: int = self.game._config.screen_width - self.x_offset
        self.height: int = self.game._config.screen_height - self.y_offset

        level_bar_x: int = self.x_offset + round(self.width * 0.07)
        level_bar_y: int = self.y_offset
        level_bar_width: int = round(self.width*0.88)
        level_bar_height: int = round(self.height*0.03)

        self.game._player.set_level_text = self.set_level_text

        self.level_bar: Bar = Bar(
            Color(*self.game._config.level_bar_color),
            Color(*self.game._config.level_bar_border_color),
            Position(level_bar_x, level_bar_y),
            level_bar_width,
            level_bar_height,
            1,
            100,
            progression=0,
            is_dynamic=True,
            smooth_end=True,
        )

        self.game._player._level_bar = self.level_bar

        self.level_text: FontSequence = FontSequence(
            "Null",
            self.game._font,
            Color(*self.game._config.level_bar_color),
            Position(level_bar_x - round(self.width * 0.01), level_bar_y + level_bar_height),
            spacing=1,
            align=AlignEnum.RIGHT,
            is_dynamic=True
        )

        # TODO connect level_text with player level

        self.timer: FontSequence = FontSequence(
            "Null",
            self.game._font,
            Color(*self.game._config.timer_color),
            Position(
                    self.x_offset + round(self.width / 2),
                    self.y_offset + round(self.height*0.07)
                ),
            spacing=1,
            is_dynamic=True
        )

        self.set_timer(600)

        maze_x = self.x_offset + round(self.width * 0.02)
        maze_y = self.y_offset + level_bar_height + round(self.height * 0.07)

        available_width = self.width - round(self.width * 0.07)
        available_height = (
            self.height
            - level_bar_height
            - round(self.height * 0.11)
        )

        maze_base_width = self.game._level.get_width()
        maze_base_height = self.game._level.get_height()

        scale = min(
            available_width / maze_base_width,
            available_height / maze_base_height,
        )

        maze_width = round(maze_base_width * scale)
        maze_height = round(maze_base_height * scale)

        maze_x += (available_width - maze_width) // 2
        maze_y += (available_height - maze_height) // 2

        self.maze: MeshLevel = MeshLevel(
            self.game._level,
            Color(*self.game._config.maze_color),
            Position(maze_x, maze_y),
            maze_width,
            maze_height,
            wall_thickness=3,
            is_dynamic=True,
            smooth_end=True
        )

        self.maze.register_entities_to_screen()

        self.layer.meshes.append(self.level_bar)
        self.layer.meshes.append(self.level_text)
        self.layer.meshes.append(self.timer)
        self.layer.meshes.append(self.maze)

    @staticmethod
    def sec_to_str(seconds: int) -> str:
        return f"{seconds//60:02}:{seconds%60:02}"

    def set_level_text(self, level: int) -> None:
        self.level_text.set_sequence_text(f"Lvl .{level}")

    def set_level_bar_progression(self, progression: int) -> None:
        self.level_bar.set_progression(progression)

    def set_level_bar_goal(self, goal: int) -> None:
        self.level_bar.set_goal(goal)

    def set_timer(self, seconds: int) -> None:
        self.timer_value: int = seconds
        self.refresh_timer()

    def refresh_timer(self, dt: int = 0) -> None:
        self.timer_value += dt
        self.timer.set_sequence_text(self.sec_to_str(self.timer_value))

    def get_layer(self) -> MeshLayer:
        return self.layer
