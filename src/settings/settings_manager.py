from pathlib import Path

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
                f.write(self._settings.model_dump_json())
                return True
        except (OSError, RuntimeError, ValueError) as e:
            self._logger.warning(f'Cannot save settings : {e!s}')
        return False

    def get(self) -> SettingsModel:
        return self._settings
