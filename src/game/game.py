from random import randint

import pygame
from pygame.event import Event
from pygame.time import Clock

from src.app import App
from src.config import ConfigModel
from src.config.level_model import FIRST_LEVEL_SEED, LevelModel
from src.core import EventHandler, Level, Timer
from src.core.displayable import Displayable
from src.core.interface_manager import InterfaceManager
from src.game.ameliorations.amelioration import Amelioration
from src.game.characters import (
    BlinkyGhost,
    ClydeGhost,
    Ghost,
    InkyGhost,
    PinkyGhost,
    Player,
)
from src.game.game_status import GameStatus, InterfaceStatus
from src.game.items import PacGum, SuperPacGum
from src.graphics.screen import Screen
from src.ui import (
    AmeliorationInterface,
    EscapeInterface,
    GameInterface,
    StatsInterface,
)
from src.ui.cheat_interface import CheatInterface
from src.ui.gameover_interface import GameoverInterface
from src.ui.how_to_play_interface import HowToPLayInterface
from src.ui.leaderboard_interface import LeaderboardInterface
from src.ui.lobby_interface import LobbyInterface
from src.ui.save_run_interface import SaveRunInterface
from src.ui.settings_interface import SettingsInterface
from src.ui.victory_interface import VictoryInterface
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
    _status_history: list[GameStatus]
    _config: ConfigModel
    _status: GameStatus
    _screen: Screen
    _level: Level
    _clock: Clock
    _player: Player
    _freeze_ghost: bool
    _timer: Timer
    _level_index: int
    _score: float
    _time_survived: float
    _ghosts_defeated: int
    _pellets_eaten: int
    _howtoplay_interface: HowToPLayInterface
    _leaderboard_interface: LeaderboardInterface
    _victory_interface: VictoryInterface
    _settings_interface: SettingsInterface
    _lobby_interface: LobbyInterface
    _save_run_interface: SaveRunInterface

    def __init__(self, config: ConfigModel, screen: Screen, app: App) -> None:
        """
        Initialize the instance.

        Args:
            config: Configuration values used to initialize the component.
            screen: Display surface used for rendering.
            app: Application instance that owns the object.
        """
        self._app = app
        self._logger = Logger(name='Game', color=TColor.CYAN, verbose=True)

        self._app.settings.refresh_screen_resolution()

        self._interface_manager = InterfaceManager(self)

        self._status_history = []
        self._status = GameStatus.IDLE
        self.set_interface_status(InterfaceStatus.LOBBY)

        self._level_index = 0
        self._score = 0
        self._time_survived = 0
        self._ghosts_defeated = 0
        self._pellets_eaten = 0

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
        """
        Initialize the associated state.
        """
        self._timer = Timer(self._config.levels[self._level_index].max_time)
        self._timer.set_cb_update(self._game_interface.refresh_timer)
        self._timer.set_cb_finish(lambda: self.set_status(GameStatus.GAMEOVER))

    def toggle_freeze(self, value: bool) -> None:
        """
        Handle toggle freeze.

        Args:
            value: Value to assign or apply.
        """
        self._freeze_ghost = value
        for ghost in self._level._entities.gets(Ghost):
            ghost.set_freeze(self._freeze_ghost)

    def toggle_wallhack(self, value: bool) -> None:
        """
        Handle toggle wallhack.

        Args:
            value: Value to assign or apply.
        """
        self._player._wallhack = value

    def toggle_noclip(self, value: bool) -> None:
        """
        Handle toggle noclip.

        Args:
            value: Value to assign or apply.
        """
        self._player._noclip = value

    def toggle_godmod(self, value: bool) -> None:
        """
        Handle toggle godmod.

        Args:
            value: Value to assign or apply.
        """
        self._player._godmod = value

    def get_freeze_status(self) -> bool:
        """
        Return the current freeze status.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        return self._freeze_ghost

    def get_wallhack_status(self) -> bool:
        """
        Return the current wallhack status.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        return self._player._wallhack

    def get_noclip_status(self) -> bool:
        """
        Return the current noclip status.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        return self._player._noclip

    def get_godmod_status(self) -> bool:
        """
        Return the current godmod status.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        return self._player._godmod

    def set_status(self, status: GameStatus, remember: bool = True) -> None:
        """
        Assign the status.

        Args:
            status: New state to assign to the object.
            remember: Remember used by the operation.
        """
        if remember and self._status is not status:
            self._status_history.append(self._status)

        self._status = status
        interface_status = {
            GameStatus.RUNNING: InterfaceStatus.RUNNING,
            GameStatus.PAUSED: InterfaceStatus.PAUSED,
            GameStatus.INITIALIZING: InterfaceStatus.INITIALIZING,
            GameStatus.AMELIORATION: InterfaceStatus.AMELIORATION,
            GameStatus.VICTORY: InterfaceStatus.VICTORY,
            GameStatus.GAMEOVER: InterfaceStatus.GAMEOVER,
            GameStatus.CHEAT_MENU: InterfaceStatus.CHEAT_MENU,
        }.get(status)
        if interface_status is not None:
            self._interface_manager.set_status(interface_status)

        if status in (GameStatus.GAMEOVER, GameStatus.VICTORY):
            rank = self._app.leaderboard.snapshot(round(self._score))
            if rank is not None:
                self.set_interface_status(InterfaceStatus.SAVE_RUN)

    def set_back_status(self) -> bool:
        """
        Assign the back status.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        if not self._status_history:
            return False

        self.set_status(self._status_history.pop(), remember=False)
        return True

    def set_interface_status(self, status: InterfaceStatus) -> None:
        """
        Assign the interface status.

        Args:
            status: New state to assign to the object.
        """
        self._interface_manager.set_status(status)

    def get_interface_status(self) -> InterfaceStatus | None:
        """
        Return the current interface status.

        Returns:
            The current interface status.
        """
        return self._interface_manager.get_status()

    def get_status(self) -> GameStatus:
        """
        Return the current status.

        Returns:
            The current status.
        """
        return self._status

    def generate_level(self) -> None:
        """
        Handle generate level.
        """
        self._level.generate(
            self._config.levels[self._level_index]
        )

    def next_level(self) -> None:
        """
        Handle next level.
        """
        if self._level_index + 1 >= len(self._config.levels):
            self.set_status(GameStatus.VICTORY)
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

    def prev_level(self) -> None:
        """
        Handle prev level.
        """
        self._level_index = max(self._level_index - 1, 0)

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
        """
        Handle update.

        Args:
            dt: Elapsed time since the previous update, in seconds.
        """
        self._time_survived += dt
        self._timer.update(dt)
        self._level.update(dt)
        self.refresh_maze()
        self._stats_interface.refresh()
        self._screen.refresh()
        self._game_interface.refresh(dt)
        if self.get_status() in [
            GameStatus.RUNNING,
            GameStatus.INITIALIZING
        ] and self._level.is_finished():
            self.next_level()

        if self.get_status() in [
            GameStatus.RUNNING,
            GameStatus.INITIALIZING
        ] and not self._player.alive:
            self._player.on_death()
            if self._player.over:
                self.set_status(GameStatus.GAMEOVER)
                pygame.display.flip()
                return

            self._player._direction = None
            self._player._progress = 0
            self._player._target = None
            self._player._queued = None
            self._player.set_tile(self._player_start_position)

            for ghost in self._ghosts:
                ghost._target = None
                ghost.tile = ghost.get_spawn_tile()
            self.set_status(GameStatus.INITIALIZING)

        pygame.display.flip()

    def record_collection(self, reward: float, ghost: bool = False) -> None:
        """
        Handle record collection.

        Args:
            reward: Reward used by the operation.
            ghost: Ghost used by the operation.
        """
        self._score += reward
        if ghost:
            self._ghosts_defeated += 1
        else:
            self._pellets_eaten += 1

    def get_score(self) -> int:
        """
        Return the current score.

        Returns:
            The current score.
        """
        return round(self._score)

    def get_victory_values(self) -> tuple[int, int, int, int, int]:
        """
        Return the current victory values.

        Returns:
            The current victory values.
        """
        return (
            self.get_score(),
            round(self._time_survived),
            self._player._actual_level,
            self._ghosts_defeated,
            self._pellets_eaten,
        )

    def refresh_maze(self) -> None:
        """
        Handle refresh maze.
        """
        for e in self._level._to_register:
            self._game_interface.maze.register_entity(e)
        self._level._to_register = []
        for e in self._level._to_unregister:
            self._game_interface.maze.unregister_entity(e)
        self._level._to_unregister = []

    def init_entities(self, player: Player | None = None) -> None:
        """
        Initialize the associated state.

        Args:
            player: Player used by the operation.
        """
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
        """
        Initialize the associated state.
        """
        Amelioration._app = self._app

        self._game_interface = GameInterface(self)
        self._stats_interface = StatsInterface(self)
        self._escape_interface = EscapeInterface(self)
        self._amelioration_interface = AmeliorationInterface(self)
        self._cheat_interface = CheatInterface(self)
        self._victory_interface = VictoryInterface(self)
        self._gameover_interface = GameoverInterface(self)
        self._victory_interface = VictoryInterface(self)
        self._settings_interface = SettingsInterface(self)
        self._leaderboard_interface = LeaderboardInterface(self)
        self._howtoplay_interface = HowToPLayInterface(self)
        self._lobby_interface = LobbyInterface(self)
        self._save_run_interface = SaveRunInterface(self)

        gameplay_statuses: list[InterfaceStatus] = [
            InterfaceStatus.RUNNING,
            InterfaceStatus.INITIALIZING,
            InterfaceStatus.PAUSED,
            InterfaceStatus.AMELIORATION,
            InterfaceStatus.CHEAT_MENU,
            InterfaceStatus.VICTORY,
            InterfaceStatus.GAMEOVER,
            InterfaceStatus.SAVE_RUN
        ]
        self._interface_manager.set_interface(
            gameplay_statuses,
            self._game_interface
        )
        self._interface_manager.set_interface(
            gameplay_statuses,
            self._stats_interface
        )
        self._interface_manager.set_interface(
            InterfaceStatus.PAUSED,
            self._escape_interface
        )
        self._interface_manager.set_interface(
            InterfaceStatus.AMELIORATION,
            self._amelioration_interface
        )
        self._interface_manager.set_interface(
            InterfaceStatus.CHEAT_MENU,
            self._cheat_interface
        )
        self._interface_manager.set_interface(
            InterfaceStatus.VICTORY,
            self._victory_interface
        )
        self._interface_manager.set_interface(
            InterfaceStatus.GAMEOVER,
            self._gameover_interface
        )
        self._interface_manager.set_interface(
            InterfaceStatus.VICTORY,
            self._victory_interface
        )
        self._interface_manager.set_interface(
            InterfaceStatus.SAVE_RUN,
            self._save_run_interface
        )
        self._interface_manager.set_interface(
            InterfaceStatus.HOWTOPLAY,
            self._howtoplay_interface
        )
        self._interface_manager.set_interface(
            InterfaceStatus.LEADERBOARD,
            self._leaderboard_interface
        )
        self._interface_manager.set_interface(
            InterfaceStatus.SETTINGS,
            self._settings_interface
        )
        self._interface_manager.set_interface(
            InterfaceStatus.LOBBY,
            self._lobby_interface
        )

        self._screen.add_mesh(self._lobby_interface)
        self._screen.add_mesh(self._game_interface)
        self._screen.add_mesh(self._stats_interface)
        self._screen.add_mesh(self._escape_interface)
        self._screen.add_mesh(self._amelioration_interface)
        self._screen.add_mesh(self._cheat_interface)
        self._screen.add_mesh(self._victory_interface)
        self._screen.add_mesh(self._gameover_interface)
        self._screen.add_mesh(self._victory_interface)
        self._screen.add_mesh(self._howtoplay_interface)
        self._screen.add_mesh(self._leaderboard_interface)
        self._screen.add_mesh(self._settings_interface)
        self._screen.add_mesh(self._save_run_interface)
        self._interface_manager.refresh_interfaces()

    def run(self) -> None:
        """
        Handle run.
        """
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

            self.update(dt)

    def exit(self) -> None:
        """
        Handle exit.
        """
        self.set_status(GameStatus.EXIT)

    def launch_new_run(self) -> None:
        """
        Handle launch new run.
        """
        self._level_index = 0
        self._score = 0
        self._time_survived = 0
        self._ghosts_defeated = 0
        self._pellets_eaten = 0

        self.set_status(GameStatus.INITIALIZING)
        self._init_level()
        self.generate_level()
        self.init_entities()
        self._game_interface.update_level()
        self._stats_interface.clear_ameliorations()
        self._stats_interface.refresh()
        self.init_timer()
        self.toggle_freeze(False)

    def _on_exit(self, _: Event, __: int) -> None:
        """
        Handle on exit.
        """
        self.exit()

    def _init_level(self) -> None:
        """
        Create the level at the current index.

        The seed comes from the configuration. When it is omitted, the
        first level uses a fixed seed and the next ones a random seed.
        """
        level: LevelModel = self._config.levels[self._level_index]
        seed: int | None = level.seed
        if seed is None:
            seed = (
                FIRST_LEVEL_SEED
                if self._level_index == 0
                else randint(1, 2 ** 31 - 1)
            )
        self._logger.log(f'Level {self._level_index + 1} seed: {seed}')
        self._level = Level(level, seed)

    def _init_screen(self) -> None:
        """
        Handle init screen.
        """
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
        self._event_handler.register_listener(
            pygame.VIDEORESIZE, self._on_resize
        )

    def _on_resize(self, event: Event, _: int) -> None:
        """
        Handle on resize.

        Args:
            event: Pygame event being handled.
        """
        self._screen.resize(event.w, event.h)

    def _on_key_down(self, event: Event, _: int) -> None:
        """
        Handle on key down.

        Args:
            event: Pygame event being handled.
        """
        for interface in self._interface_manager.get_interfaces():
            if interface.handle_key(event.key):
                return

    def load_pack(self, path: str) -> None:
        """
        Load the associated data.

        Args:
            path: Filesystem path used to load or save the data.
        """
        self._app.texture.load_pack(path)

        for e in self._level.store.all():
            if not isinstance(e, Displayable):
                continue
            e.init_displayable()

    def unload_pack(self) -> None:
        """
        Handle unload pack.
        """
        self._app.texture.unload_pack()

        for e in self._level.store.all():
            if not isinstance(e, Displayable):
                continue
            e.init_displayable()

    def _init_event_handler(self) -> None:
        """
        Handle init event handler.
        """
        self._event_handler = EventHandler()

    def _set_config(self, config: ConfigModel) -> None:
        """
        Handle set config.

        Args:
            config: Configuration values used to initialize the component.
        """
        self._config = config

    def _set_screen(self, screen: Screen) -> None:
        """
        Handle set screen.

        Args:
            screen: Display surface used for rendering.
        """
        self._screen = screen
