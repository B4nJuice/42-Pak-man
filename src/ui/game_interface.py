from typing import TYPE_CHECKING, cast

import pygame

from src.game.game_status import GameStatus, InterfaceStatus
from src.settings import ActionKey

if TYPE_CHECKING:
    from src.game import Game

from src.app import App
from src.core.displayable import DisplayableEntity
from src.graphics import Color, Plane, Position
from src.graphics.mesh_layer import MeshLayer
from src.graphics.super_meshes import AlignEnum, Bar, FontSequence, MeshLevel

from ..fonts.font_manager import FontKey
from .interface import Interface


class GameInterface(Interface):
    def __init__(self, game: 'Game') -> None:
        super().__init__(game)

        self.app: App = game._app
        self.game: Game = game
        self.layer: MeshLayer = MeshLayer()

        self.x_offset: int = round(self.game._config.screen_width * 0.25)
        self.y_offset: int = round(self.game._config.screen_height * 0.02)
        self.width: int = self.game._config.screen_width - self.x_offset
        self.height: int = self.game._config.screen_height - self.y_offset

        level_bar_x: int = self.x_offset + round(self.width * 0.07)
        level_bar_y: int = self.y_offset
        level_bar_width: int = round(self.width * 0.88)
        level_bar_height: int = round(self.height * 0.03)

        self.game._player.set_level_text = self.set_level_text

        self.background = Plane(
            Color(*self.game._config.background),
            (
                Position(0, 0),
                Position(
                    self.game._config.screen_width,
                    self.game._config.screen_height
                )
            )
        )

        self.level_bar: Bar = Bar(
            Color(*self.game._config.level_bar_color),
            Color(*self.game._config.level_bar_border_color),
            Position(level_bar_x, level_bar_y),
            level_bar_width,
            level_bar_height,
            border_thickness=2,
            goal=100,
            progression=0,
            smooth_end=True,
        )

        self.game._player._level_bar = self.level_bar

        self.level_text: FontSequence = FontSequence(
            "Lv. 0",
            self.app.fonts.get(FontKey.TITLE_24),
            Color(*self.game._config.level_bar_color),
            Position(
                level_bar_x - round(self.width * 0.01),
                level_bar_y + level_bar_height - 2
            ),
            spacing=1,
            align=AlignEnum.RIGHT,
        )

        self.timer: FontSequence = FontSequence(
            "Null",
            self.app.fonts.get(FontKey.TITLE_24),
            Color(*self.game._config.timer_color),
            Position(
                    self.x_offset + round(self.width / 2),
                    self.y_offset + round(self.height*0.07)
                ),
            spacing=1,
        )

        self.maze: MeshLevel = self._create_maze(level_bar_height)

        self.layer.meshes.append(self.background)
        self.layer.meshes.append(self.level_bar)
        self.layer.meshes.append(self.level_text)
        self.layer.meshes.append(self.timer)
        self.layer.meshes.append(self.maze)

    @staticmethod
    def sec_to_str(seconds: float) -> str:
        return f"{int(seconds//60):02}:{int(seconds) % 60:02}"

    def set_level_text(self, level: int) -> None:
        self.level_text.set_sequence_text(f"LV. {level}")

    def set_level_bar_progression(self, progression: float) -> None:
        self.level_bar.set_progression(progression)

    def set_level_bar_goal(self, goal: float) -> None:
        self.level_bar.set_goal(goal)

    def _create_maze(self, level_bar_height: int | None = None) -> MeshLevel:
        if level_bar_height is None:
            level_bar_height = round(self.height * 0.03)

        maze_x = self.x_offset + round(self.width * 0.02)
        maze_y = self.y_offset + level_bar_height + round(self.height * 0.07)
        available_width = self.width - round(self.width * 0.07)
        available_height = self.height - level_bar_height - round(
            self.height * 0.11
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

        return MeshLevel(
            self.game._level,
            Color(*self.game._config.maze_wall_color),
            Color(*self.game._config.maze_backgroud_color),
            Position(maze_x, maze_y),
            maze_width,
            maze_height,
            wall_thickness=3,
            smooth_end=True
        )

    def update_level(self) -> None:
        old_maze = self.maze
        self.maze = self._create_maze()
        self.layer.meshes[self.layer.meshes.index(old_maze)] = self.maze

        self.game._player.set_level_text = self.set_level_text
        self.game._player._level_bar = self.level_bar
        for entity in self.game._level.store.all():
            if hasattr(entity, 'set_mesh_level_position'):
                self.maze.register_entity(cast(DisplayableEntity, entity))
        self.game._level._to_register = []
        self.game._level._to_unregister = []

    def refresh_timer(self, value: float) -> None:
        self.timer.set_sequence_text(self.sec_to_str(max(value, 0.0)))

    def refresh(self, _: float) -> None:
        self.maze.refresh()

    def get_layer(self) -> MeshLayer:
        return self.layer

    def handle_key(self, key: int) -> bool:
        match key:
            case pygame.K_F1:
                self.game._cheat_interface.action_toggle()

        if self.game.get_status() not in [
            GameStatus.RUNNING,
            GameStatus.INITIALIZING
        ] or self.game.get_interface_status() in [
            InterfaceStatus.CHEAT_MENU,
            InterfaceStatus.AMELIORATION
        ]:
            return False

        if key in self.game._app.key_manager.get_keys(
            ActionKey.BACK_PAUSE_RESUME
        ):
            self.game.set_status(GameStatus.PAUSED)
            return True

        return super().handle_key(key)
