import pygame
from pygame.event import Event
from pygame.time import Clock

from src.app import App
from src.config import ConfigModel
from src.core import EventHandler, Level
from src.core.displayable import Displayable
from src.errors import PackError
from src.game.characters import (
    BlinkyGhost,
    ClydeGhost,
    InkyGhost,
    PinkyGhost,
    Player,
)
from src.game.game_status import GameStatus
from src.game.items import PacGum, SuperPacGum
from src.graphics.font import Font
from src.graphics.screen import Screen
from src.texture.font_keys import FontKeys
from src.ui import (
    AmeliorationInterface,
    EscapeInterface,
    GameInterface,
    StatsInterface,
)
from src.utils import Logger, TColor


class Game:
    _app: App
    _logger: Logger
    _player_start_position: tuple[int, int]
    _amelioration_interface: AmeliorationInterface
    _escape_interface: EscapeInterface
    _stats_interface: StatsInterface
    _game_interface: GameInterface
    _event_handler: EventHandler
    _config: ConfigModel
    _status: GameStatus
    _screen: Screen
    _level: Level
    _clock: Clock
    _font: Font
    _player: Player

    def __init__(self, config: ConfigModel, screen: Screen, app: App) -> None:
        self._app = app
        self._logger = Logger(name='Game', color=TColor.CYAN, verbose=True)
        self.set_status(GameStatus.INITIALIZING)

        self._set_config(config)
        self._set_screen(screen)

        self._font = Font(
            self._app.texture.get_font(FontKeys.DEFAULT).as_posix(),
            self._screen.moderngl_context,
            pixel_size=self._config.screen_height // 22
        )

        self._init_level()
        self._init_event_handler()
        self._init_screen()
        self.generate_level()

        self.init_entities()
        self.init_interfaces()

    def set_status(self, status: GameStatus) -> None:
        self._status = status

    def get_status(self) -> GameStatus:
        return self._status

    def generate_level(self) -> None:
        self._level.generate(
            self._config.level_width,
            self._config.level_height
        )

    def update(self, dt: float) -> None:
        self._level.update(dt)
        self.refresh_maze()
        self._screen.refresh()
        self._game_interface.refresh(dt)

        if not self._player.alive:
            self._player.on_death()
            self._player._direction = None
            self._player._progress = 0
            self._player._target = None
            self._player._queued = None
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
                    self._config.pacgum_reward,
                    self._app
                )

        for pos in super_pacgum_positions:
            SuperPacGum(
                'super_pacgum',
                pos,
                self._level,
                self._config.super_pacgum_reward,
                self._app
            )

        self._player_start_position = (
                self._level.get_width()//2 - 1, self._level.get_height()//2 - 1
            )

        self._player = Player(
            'player',
            self._player_start_position,
            self._level,
            self._config.player_level_exp_multiplier,
            self._config.player_first_level_exp,
            self._config.player_exp_per_second,
            self._app,
            self
        )

        ghost_reward: float = self._config.ghost_reward

        self._ghost_1 = BlinkyGhost(
            0,
            (0, 0),
            self._level,
            ghost_reward,
            app=self._app
        )
        self._ghost_2 = PinkyGhost(
            0,
            (self._level.get_width() - 1, 0),
            self._level,
            ghost_reward,
            app=self._app
        )
        self._ghost_3 = InkyGhost(
            0,
            (self._level.get_width() - 1, self._level.get_height() - 1),
            self._level,
            ghost_reward,
            app=self._app
        )
        self._ghost_4 = ClydeGhost(
            0,
            (0, self._level.get_height() - 1),
            self._level,
            ghost_reward,
            app=self._app
        )

    def init_interfaces(self) -> None:
        self._game_interface = GameInterface(self)
        self._stats_interface = StatsInterface(self)
        self._escape_interface = EscapeInterface(self)
        self._amelioration_interface = AmeliorationInterface(self)

        self._screen.add_mesh(self._game_interface)
        self._screen.add_mesh(self._stats_interface)
        self._screen.add_mesh(self._escape_interface)
        self._screen.add_mesh(self._amelioration_interface)

    def run(self) -> None:
        # self.set_status(GameStatus.RUNNING)
        dt: float = 0.0

        self.update(dt)
        while self.get_status() != GameStatus.EXIT:
            for event in pygame.event.get():
                self._event_handler.dispatch_event(event, event.type)

            if self.get_status() != GameStatus.RUNNING:
                dt = 0

            if self._player.over:
                break

            self.update(dt)
            dt = self._clock.tick(120.0) / 1000

    def exit(self) -> None:
        self.set_status(GameStatus.EXIT)

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
        self._event_handler.register_listener(
            pygame.MOUSEBUTTONUP, self._screen.click
        )

    def _on_key_down(self, event: Event, _: int) -> None:
        match event.key:
            case pygame.K_ESCAPE:
                if self.get_status() == GameStatus.PAUSED:
                    self._escape_interface.end()
                else:
                    self._escape_interface.start()

            case pygame.K_F1:
                self._player._cheat = not self._player._cheat
            case pygame.K_F9:
                try:
                    self.load_pack('textures/reverse-textures')
                except PackError as e:
                    self._logger.warning(
                        f'Cannot load ressource pack: {str(e)!r}'
                    )
            case pygame.K_F10:
                self.unload_pack()

    def load_pack(self, path: str) -> None:
        self._app.texture.load_pack(path)

        for e in self._level.store.all():
            if not isinstance(e, Displayable):
                continue
            e.init_displayable()

    def unload_pack(self) -> None:
        self._app.texture.unload_pack()

        for e in self._level.store.all():
            if not isinstance(e, Displayable):
                continue
            e.init_displayable()

    def _init_event_handler(self) -> None:
        self._event_handler = EventHandler()

    def _set_config(self, config: ConfigModel) -> None:
        self._config = config

    def _set_screen(self, screen: Screen) -> None:
        self._screen = screen
