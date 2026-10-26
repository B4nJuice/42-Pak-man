import hashlib
import hmac
import secrets
from pathlib import Path

from pydantic import ValidationError

from src.leaderboard.leaderboard_models import (
    LeaderboardEntryModel,
    LeaderboardModel,
)
from src.utils import Logger, TColor

DEFAULT_PATH = '.pak-man/highscore.json'
SECRET_PATH = '.pak-man/.secret'


class LeaderboardCore:
    _logger: Logger
    _path: str
    _secret: bytes | None
    _leaderboard: LeaderboardModel

    def __init__(
                self,
                path: str = DEFAULT_PATH,
                verbose: bool = False
            ) -> None:
        self._logger = Logger(
            name='Leaderboard',
            color=TColor.BRIGHT_YELLOW,
            verbose=verbose
        )
        self.set_path(path)
        self._secret = None

        self._logger.log(f'Loading leaderboard from: {self._path!r}')
        self.load()

    def add(self, entry: LeaderboardEntryModel) -> bool:
        added: bool = self._leaderboard.add(entry)
        if added:
            self.save()
        return added

    def get(self) -> list[LeaderboardEntryModel]:
        return self._leaderboard.entries

    def save(self) -> bool:
        try:
            path = Path(self._path)
            path.parent.mkdir(parents=True, exist_ok=True)
            self._leaderboard.sig = self._leaderboard.compile(
                self._hash_function,
                self._get_first_hash(),
            )

            with open(path, 'w', encoding='UTF-8') as f:
                f.write(self._leaderboard.model_dump_json())

                return True
        except (OSError, RuntimeError, ValueError) as e:
            self._logger.warning(f'Cannot save leaderboard : {e!s}')
        return False

    def load(self) -> None:
        leaderboard = self._load_leaderboard_file()

        if leaderboard is None:
            self._logger.log(
                f'No valid leaderboard found at {self._path!r}; '
                'creating empty one.'
            )
            leaderboard = self._generate_empty_leaderboard()
            leaderboard.clean()
            self._leaderboard = leaderboard
            self.save()
        else:
            leaderboard.clean()
            self._leaderboard = leaderboard

        self._logger.info(
            f'Leaderboard loaded with {len(self._leaderboard.entries)}'
            ' entries.'
        )

    def _load_leaderboard_file(self) -> LeaderboardModel | None:
        try:
            with open(self._path, 'r', encoding='utf-8') as f:
                leaderboard = LeaderboardModel.model_validate_json(f.read())
                if leaderboard.verify(
                    self._hash_function,
                    self._get_first_hash()
                ):
                    return leaderboard
                self._logger.warning(
                    'Leaderboard signature is invalid; ignoring file.'
                )
        except (ValidationError, ValueError):
            self._logger.warning(
                f'Leaderboard file at {self._path!r} is malformed or '
                'corrupted.'
            )
        except (OSError, RuntimeError):
            self._logger.log(f'Leaderboard file not found at {self._path!r}.')

        return None

    def _generate_empty_leaderboard(self) -> LeaderboardModel:
        return LeaderboardModel()

    def get_secret(self) -> bytes:
        if self._secret is None:
            self._load_secret()

        if self._secret is None:
            self._secret = self.generate_secret()
            self._save_secret()

        return self._secret

    def _load_secret(self) -> None:
        try:
            with open(SECRET_PATH, 'r') as f:
                secret = f.read()
                if len(secret.strip()) > 0:
                    self._secret = secret.encode()

        except (OSError, RuntimeError):
            pass

    def _save_secret(self) -> None:
        try:
            Path(self._path).parent.mkdir(exist_ok=True)
            with open(SECRET_PATH, 'w', encoding='UTF-8') as f:
                f.write(self.get_secret().decode())

        except (OSError, RuntimeError) as e:
            print(e)

    def generate_secret(self) -> bytes:
        return secrets.token_hex(nbytes=16).encode('utf-8')

    def _hash_function(self, payload: bytes) -> str:
        return hmac.new(self.get_secret(), payload, hashlib.sha256).hexdigest()

    def _get_first_hash(self) -> str:
        return self._hash_function(b'None|0|' + self.get_secret())

    def set_path(self, path: str) -> None:
        normalized_path = str(Path(path).expanduser().resolve())
        self._path = normalized_path
