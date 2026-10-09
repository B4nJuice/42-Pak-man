import pygame
from pygame.event import Event
from pygame.time import Clock

from src.config import ConfigModel
from src.core import EventHandler, Level
from src.graphics.font import Font

from src.graphics.screen import Screen
from src.ui import GameInterface, StatsInterface, EscapeInterface
from src.game.characters import Ghost, Player
from src.game.items import PacGum, SuperPacGum
from src.game.game_state import GameState


class Game:
    _player_start_position: tuple[int, int]
    _escape_interface: EscapeInterface
    _stats_interface: StatsInterface
    _game_interface: GameInterface
    _event_handler: EventHandler
    _config: ConfigModel
    _state: GameState
    _screen: Screen
    _level: Level
    _clock: Clock
    _font: Font

    def __init__(self, config: ConfigModel, screen: Screen) -> None:
        self.set_state(GameState.INITIALIZING)

        self._set_config(config)
        self._set_screen(screen)

        self._font = Font(
                self._config.font_path,
                self._screen.moderngl_context,
                pixel_size=self._config.screen_height // 22
            )

        self._init_level()
        self._init_event_handler()
        self._init_screen()
        self.generate_level()

        self.init_entities()
        self.init_interfaces()

    def set_state(self, state: GameState) -> None:
        self._state = state

    def get_state(self) -> GameState:
        return self._state

    def generate_level(self) -> None:
        self._level.generate(
            self._config.level_width,
            self._config.level_height
        )

    def update(self, dt: float) -> None:
        self._level.update(dt)
        self.refresh_maze()
        self._screen.refresh()

        if not self._player.alive:
            self._player.on_death()
            self._player.set_tile(self._player_start_position)

        pygame.display.flip()

    def refresh_maze(self) -> None:
        for e in self._level._to_register:
            self._game_interface.maze.register_entity(e)
        self._level._to_register = []
        for e in self._level._to_unregister:
            self._game_interface.maze.unregister_entity(e)
        self._level._to_unregister = []

    def init_entities(self) -> None:
        super_pacgum_positions: list[tuple[int, int]] = [
            (0, 0),
            (self._level.get_width() - 1, 0),
            (self._level.get_width() - 1, self._level.get_height() - 1),
            (0, self._level.get_height() - 1)
        ]

        for x in range(self._level.get_width()):
            for y in range(self._level.get_height()):
                if (x, y) in super_pacgum_positions:
                    continue
                if self._level.get_tile(x, y).is_full:
                    continue
                PacGum(
                    'pacgum',
                    (x, y),
                    self._level,
                    self._config.pacgum_reward
                )

        for pos in super_pacgum_positions:
            SuperPacGum(
                'super_pacgum',
                pos,
                self._level,
                self._config.super_pacgum_reward
            )

        self._player_start_position = (
                self._level.get_width()//2 - 1, self._level.get_height()//2 - 1
            )
        self._player = Player(
                'player',
                self._player_start_position,
                self._level
            )

        self._ghost_1 = Ghost(
            'test',
            (0, 1),
            self._level,
            self._config.ghost_reward
        )

    def init_interfaces(self) -> None:
        self._game_interface = GameInterface(self)
        self._stats_interface = StatsInterface(self)
        self._escape_interface = EscapeInterface(self)

        self._screen.add_mesh(self._game_interface)
        self._screen.add_mesh(self._stats_interface)
        self._screen.add_mesh(self._escape_interface)

    def run(self) -> None:
        self.set_state(GameState.RUNNING)
        dt: float = 0.0

        self.update(dt)
        while self.get_state() != GameState.EXIT:
            for event in pygame.event.get():
                self._event_handler.dispatch_event(event, event.type)

            if self.get_state() == GameState.PAUSED:
                dt = 0

            if self._player.over:
                break

            self.update(dt)
            dt = self._clock.tick(60.0) / 1000

    def exit(self) -> None:
        self.set_state(GameState.EXIT)

    def _on_exit(self, _: Event, __: int) -> None:
        self.exit()

    def _init_level(self) -> None:
        self._level = Level(1)

    def _init_screen(self) -> None:
        self._clock = Clock()
        self._running = False
        self._event_handler.register_listener(pygame.QUIT, self._on_exit)
        self._event_handler.register_listener(
            pygame.KEYDOWN, self._on_key_down
        )

    def _on_key_down(self, event: Event, _: int) -> None:
        if event.key == pygame.K_ESCAPE:
            self.set_state(
                GameState.RUNNING if self.get_state() ==
                GameState.PAUSED else GameState.PAUSED
            )
            if self.get_state() == GameState.PAUSED:
                self._escape_interface.display()
            else:
                self._escape_interface.hide()
            # self.exit()

    def _init_event_handler(self) -> None:
        self._event_handler = EventHandler()

    def _set_config(self, config: ConfigModel) -> None:
        self._config = config

    def _set_screen(self, screen: Screen) -> None:
        self._screen = screen
