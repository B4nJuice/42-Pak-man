import pygame
from pygame.event import Event
from pygame.time import Clock

from src.app import App
from src.config import ConfigModel
from src.core import EventHandler, Level, Timer
from src.core.displayable import Displayable
from src.core.interface_manager import InterfaceManager
from src.errors import PackError
from src.game.ameliorations.amelioration import Amelioration
from src.game.characters import (
    BlinkyGhost,
    ClydeGhost,
    Ghost,
    InkyGhost,
    PinkyGhost,
    Player,
)
from src.game.game_status import GameStatus
from src.game.items import PacGum, SuperPacGum
from src.graphics.screen import Screen
from src.settings.action_key import ActionKey
from src.ui import (
    AmeliorationInterface,
    EscapeInterface,
    GameInterface,
    StatsInterface,
)
from src.ui.cheat_interface import CheatInterface

# from src.ui.victory_interface import VictoryInterface
# from src.ui.gameover_interface import GameoverInterface
# from src.ui.how_to_play_interface import HowToPLayInterface
# from src.ui.leaderboard_interface import LeaderboardInterface
from src.ui.settings_interface import SettingsInterface
from src.utils import Logger, TColor


class Game:
    _app: App
    _logger: Logger
    _player_start_position: tuple[int, int]
    _amelioration_interface: AmeliorationInterface
    _interface_manager: InterfaceManager
    _escape_interface: EscapeInterface
    _stats_interface: StatsInterface
    _game_interface: GameInterface
    _cheat_interface: CheatInterface
    _event_handler: EventHandler
    _config: ConfigModel
    _status: GameStatus
    _screen: Screen
    _level: Level
    _clock: Clock
    _player: Player
    _freeze_ghost: bool
    _timer: Timer
    _level_index: int

    _settings_interface: SettingsInterface

    def __init__(self, config: ConfigModel, screen: Screen, app: App) -> None:
        self._app = app
        self._logger = Logger(name='Game', color=TColor.CYAN, verbose=True)

        self._interface_manager = InterfaceManager(self)

        self.set_status(GameStatus.INITIALIZING)

        self._level_index = 0

        self._set_config(config)
        self._set_screen(screen)

        self._init_level()
        self._init_event_handler()
        self._init_screen()
        self.generate_level()

        self.init_entities()
        self.toggle_freeze(False)
        self.init_interfaces()
        self.init_timer()

    def init_timer(self) -> None:
        self._timer = Timer(self._config.levels[self._level_index].max_time)
        self._timer.set_cb_update(self._game_interface.refresh_timer)
        self._timer.set_cb_finish(lambda: print('player win'))

    def toggle_freeze(self, value: bool) -> None:
        self._freeze_ghost = value
        for ghost in self._level._entities.gets(Ghost):
            ghost.set_freeze(self._freeze_ghost)

    def toggle_wallhack(self, value: bool) -> None:
        self._player._wallhack = value

    def toggle_noclip(self, value: bool) -> None:
        self._player._noclip = value

    def toggle_godmod(self, value: bool) -> None:
        self._player._godmod = value

    def get_freeze_status(self) -> bool:
        return self._freeze_ghost

    def get_wallhack_status(self) -> bool:
        return self._player._wallhack

    def get_noclip_status(self) -> bool:
        return self._player._noclip

    def get_godmod_status(self) -> bool:
        return self._player._godmod

    def set_status(self, status: GameStatus) -> None:
        self._status = status
        self._interface_manager.refresh_interfaces()

    def get_status(self) -> GameStatus:
        return self._status

    def generate_level(self) -> None:
        self._level.generate(
            self._config.levels[self._level_index]
        )

    def next_level(self) -> None:
        if self._level_index + 1 >= len(self._config.levels):
            return

        self._level_index += 1
        player = self._player

        self._init_level()
        self.set_status(GameStatus.INITIALIZING)
        self.init_timer()
        self.generate_level()
        self.init_entities(player)
        self._game_interface.update_level()
        self._stats_interface.refresh()
        self.toggle_freeze(self._freeze_ghost)

    def update(self, dt: float) -> None:
        self._timer.update(dt)
        self._level.update(dt)
        self.refresh_maze()
        self._stats_interface.refresh()
        self._screen.refresh()
        self._game_interface.refresh(dt)
        if self._level.is_finished():
            self.next_level()

        if not self._player.alive:
            self._player.on_death()
            self._player._direction = None
            self._player._progress = 0
            self._player._target = None
            self._player._queued = None
            self._player.set_tile(self._player_start_position)

            for ghost in self._ghosts:
                self.set_status(GameStatus.INITIALIZING)
                ghost._target = None
                ghost.tile = ghost.get_spawn_tile()

        pygame.display.flip()

    def refresh_maze(self) -> None:
        for e in self._level._to_register:
            self._game_interface.maze.register_entity(e)
        self._level._to_register = []
        for e in self._level._to_unregister:
            self._game_interface.maze.unregister_entity(e)
        self._level._to_unregister = []

    def init_entities(self, player: Player | None = None) -> None:
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

        level_width: int = self._level.get_width()
        level_height: int = self._level.get_height()

        self._player_start_position = (
                level_width // 2 - 1 + level_width % 2,
                level_height // 2 - 1 + level_height % 2
            )

        if player is None:
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
        else:
            self._player = player
            self._player.level = self._level
            self._player.set_tile(self._player_start_position)
            self._player._direction = None
            self._player._progress = 0
            self._player._target = None
            self._player._queued = None
            self._level.register_entity(self._player)

        ghost_reward: float = self._config.ghost_reward

        self._ghosts: list[Ghost] = []

        for pos, ghost in [
            ((0, 0), BlinkyGhost),
            ((self._level.get_width() - 1, 0), PinkyGhost),
            ((self._level.get_width() - 1, self._level.get_height() - 1),
                InkyGhost),
            ((0, self._level.get_height() - 1), ClydeGhost)
        ]:
            self._ghosts.append(
                ghost(0, pos, self._level, ghost_reward, app=self._app)
            )

    def init_interfaces(self) -> None:
        Amelioration._app = self._app

        self._game_interface = GameInterface(self)
        self._stats_interface = StatsInterface(self)
        self._escape_interface = EscapeInterface(self)
        self._amelioration_interface = AmeliorationInterface(self)
        self._cheat_interface = CheatInterface(self)

        self._interface_manager.set_interface(
            GameStatus.get_all(),
            self._game_interface
        )
        self._interface_manager.set_interface(
            GameStatus.get_all(),
            self._stats_interface
        )
        self._interface_manager.set_interface(
            GameStatus.PAUSED,
            self._escape_interface
        )
        self._interface_manager.set_interface(
            GameStatus.AMELIORATION,
            self._amelioration_interface
        )
        self._interface_manager.set_interface(
            GameStatus.CHEAT_MENU,
            self._cheat_interface
        )

        self._screen.add_mesh(self._game_interface)
        self._screen.add_mesh(self._stats_interface)
        self._screen.add_mesh(self._escape_interface)
        self._screen.add_mesh(self._amelioration_interface)
        self._screen.add_mesh(self._cheat_interface)
        self._interface_manager.refresh_interfaces()

        # self._screen.add_mesh(LobbyInterface(self))
        # self._screen.add_mesh(VictoryInterface(self))
        # self._screen.add_mesh(GameoverInterface(self))
        # self._screen.add_mesh(HowToPLayInterface(self))
        # self._screen.add_mesh(LeaderboardInterface(self))
        self._settings_interface = SettingsInterface(self)
        self._screen.add_mesh(self._settings_interface)

    def run(self) -> None:
        dt: float = 0.0

        self._app.key_manager.update()
        self.update(dt)
        while self.get_status() != GameStatus.EXIT:
            dt = self._clock.tick(120.0) / 1000.0
            self._app.key_manager.update()

            for event in pygame.event.get():
                self._event_handler.dispatch_event(event, event.type)

            if self.get_status() != GameStatus.RUNNING:
                dt = 0.0

            if self._player.over:
                break

            self.update(dt)

    def exit(self) -> None:
        self.set_status(GameStatus.EXIT)

    def launch_new_run(self) -> None:
        self._logger.warning('to implement (game.py)')

    def open_leaderboard(self) -> None:
        self._logger.warning('to implement (game.py)')

    def open_settings(self) -> None:
        self._logger.warning('to implement (game.py)')

    def _on_exit(self, _: Event, __: int) -> None:
        self.exit()

    def _init_level(self) -> None:
        self._level = Level(self._config.levels[self._level_index])

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
        self._event_handler.register_listener(
            pygame.MOUSEMOTION, self._screen.hover
        )

    def _on_key_down(self, event: Event, _: int) -> None:
        if (
            self._settings_interface.handle_key(event.key) or
            self._cheat_interface.handle_key(event.key) or
            self.get_status() == GameStatus.AMELIORATION
            and self._amelioration_interface.handle_key(event.key) or
            self.get_status() == GameStatus.PAUSED
            and self._escape_interface.handle_key(event.key)
        ):
            return

        if self._app.key_manager.is_pressed_event(
            ActionKey.BACK_PAUSE_RESUME,
            event
        ):
            game_status: GameStatus = self.get_status()
            if game_status == GameStatus.PAUSED:
                self.set_status(GameStatus.RUNNING)
            elif game_status != GameStatus.AMELIORATION:
                self.set_status(GameStatus.PAUSED)

        match event.key:
            case pygame.K_F1:
                self._cheat_interface.action_toggle()
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
