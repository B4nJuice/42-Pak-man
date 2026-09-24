import pygame
from pygame.event import Event
from pygame.time import Clock

from src.config import ConfigModel
from src.core import EventHandler, Level
from src.graphics import Screen


class Game:
    _config: ConfigModel
    _level: Level
    _screen: Screen
    _running: bool
    _clock: Clock
    _event_handler: EventHandler

    def __init__(self, config: ConfigModel, screen: Screen) -> None:
        self._set_config(config)
        self._set_screen(screen)

        self._init_level()
        self._init_event_handler()
        self._init_screen()
        self.generate_level()

    def generate_level(self) -> None:
        self._level.generate(
            self._config.level_width,
            self._config.level_height
        )

    def update(self, dt: float) -> None:
        self._level.update(dt)

        self._screen.refresh()
        pygame.display.flip()

    def run(self) -> None:
        self._running = True
        dt: float = 0.0

        self.update(dt)
        while self._running:
            for event in pygame.event.get():
                self._event_handler.dispatch_event(event, event.type)

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

    def _init_event_handler(self) -> None:
        self._event_handler = EventHandler()

    def _set_config(self, config: ConfigModel) -> None:
        self._config = config

    def _set_screen(self, screen: Screen) -> None:
        self._screen = screen
