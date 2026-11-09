from pathlib import Path

import pygame
from pydantic import ValidationError

from src.settings.settings_model import SettingsModel
from src.utils import Logger, TColor


class SettingsManager:
    _path: str
    _settings: SettingsModel
    _logger: Logger

    def __init__(self, path: str, verbose: bool) -> None:
        self._path = path
        self._logger = Logger(
            name='Settings',
            color=TColor.BRIGHT_GREEN,
            verbose=verbose
        )

        self.load()

    def load(self) -> None:
        settings: SettingsModel | None = self._load_settings_from_file()

        if settings is None:
            settings = SettingsModel()

        self._settings = settings
        self._logger.info('Settings successfully loaded !')

    def refresh_screen_resolution(self) -> tuple[int, int]:
        width, height = self.get().display.resolution
        fs = pygame.FULLSCREEN if self.get().display.full_screen else 0

        max_width, max_height = pygame.display.get_desktop_sizes()[0]

        width = min(width, max_width)
        height = min(height, max_height)


        pygame.event.post(
            pygame.event.Event(
                pygame.VIDEORESIZE, size=(width, height), w=width, h=height
            )
        )

        pygame.display.set_mode(
            (width, height), pygame.OPENGL | pygame.DOUBLEBUF | fs
        )

        return width, height

    def _load_settings_from_file(self) -> SettingsModel | None:
        try:
            with open(self._path, 'r', encoding='utf-8') as f:
                return SettingsModel.model_validate_json(f.read())
        except (ValidationError, ValueError):
            self._logger.warning(
                f'Settings file at {self._path!r} is malformed or '
                'corrupted.'
            )
        except (OSError, RuntimeError):
            self._logger.log(f'Settings file not found at {self._path!r}.')

        return None

    def save(self) -> bool:
        try:
            path = Path(self._path)
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='UTF-8') as f:
                f.write(self._settings.model_dump_json(indent=4))
                return True
        except (OSError, RuntimeError, ValueError) as e:
            self._logger.warning(f'Cannot save settings : {e!s}')
        return False

    def get(self) -> SettingsModel:
        return self._settings
