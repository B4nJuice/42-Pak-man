import pygame
from pygame.event import Event
from pygame.time import Clock

from src.config import ConfigModel
from src.core import EventHandler, Level
from src.graphics.font import Font
from src.graphics.screen import Screen
from src.ui import GameInterface, StatsInterface, EscapeInterface

from .characters import Player, Ghost
from .items import PacGum


class Game:
    _config: ConfigModel
    _level: Level
    _screen: Screen
    _running: bool
    _paused: bool
    _clock: Clock
    _event_handler: EventHandler
    _font: Font
    _game_interface: GameInterface
    _stats_interface: StatsInterface
    _escape_interface: EscapeInterface

    def __init__(self, config: ConfigModel, screen: Screen) -> None:
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

    def generate_level(self) -> None:
        self._level.generate(
            self._config.level_width,
            self._config.level_height
        )

    def update(self, dt: float) -> None:
        self._level.update(dt)

        self._screen.refresh()
        pygame.display.flip()

    def init_entities(self) -> None:
        for x in range(self._level.get_width()):
            for y in range(self._level.get_height()):
                PacGum('pacgum', (x, y), self._level)
                pass
        self._player = Player('player', (
                self._level.get_width()//2 - 1, self._level.get_height()//2 - 1
            ), self._level)
        self._ghost_1 = Ghost(
            'test',
            (0, 0),
            self._level,
        )

        # self._screen.

    def init_interfaces(self) -> None:
        self._game_interface = GameInterface(self)
        self._stats_interface = StatsInterface(self)
        self._escape_interface = EscapeInterface(self)
    
        self._screen.add_mesh(self._game_interface)
        self._screen.add_mesh(self._stats_interface)
        self._screen.add_mesh(self._escape_interface)

    def run(self) -> None:
        self._running = True
        self._paused = False
        dt: float = 0.0

        self.update(dt)
        while self._running:
            for event in pygame.event.get():
                self._event_handler.dispatch_event(event, event.type)

            if self._paused:
                dt = 0

            self.update(dt)
            dt = self._clock.tick(60.0) / 1000

    def exit(self) -> None:
        self._running = False

    def _on_exit(self, _: Event, __: int) -> None:
        self.exit()

    def _init_level(self) -> None:
        self._level = Level(1)

    def _init_screen(self) -> None:
        self._clock = Clock()
        self._running = False
        self._event_handler.register_listener(pygame.QUIT, self._on_exit)
        self._event_handler.register_listener(pygame.KEYDOWN, self._on_key_down)

    def _on_key_down(self, event: Event, _: int) -> None:
        if event.key == pygame.K_ESCAPE:
            self._paused = not self._paused
            if self._paused:
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
