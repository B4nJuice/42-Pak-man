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
SECRET_FILENAME = '.secret'


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
        """
        Initialize the instance.

        Args:
            path: Filesystem path used to load or save the data.
            verbose: Whether verbose logging is enabled.
        """
        self._logger = Logger(
            name='Leaderboard',
            color=TColor.BRIGHT_YELLOW,
            verbose=verbose
        )
        self.set_path(path)
        self._secret = None

        self._logger.log(f'Loading leaderboard from: {self._path!r}')
        self.load()

    def add(
                self,
                entry: LeaderboardEntryModel
            ) -> bool:
        """
        Handle add.

        Args:
            entry: Entry used by the operation.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        added: bool = self._leaderboard.add(entry)
        if added:
            self.save()
            self._logger.info('New entry added to leaderboard.')
        return added

    def add_run(
                self,
                name: str,
                score: int,
                run_time: float,
                victory: bool
            ) -> bool:
        """
        Add the run to the collection.

        Args:
            name: Name assigned to the object or requested value.
            score: Score to record or compare.
            run_time: Run time used by the operation.
            victory: Victory used by the operation.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        return self.add(LeaderboardEntryModel(
            name=name,
            score=score,
            run_time=run_time,
            victory=victory
        ))

    def get(self) -> list[LeaderboardEntryModel]:
        """
        Handle get.

        Returns:
            The value produced by the get operation.
        """
        return self._leaderboard.entries

    def get_max_score(self) -> int:
        """
        Return the current max score.

        Returns:
            The current max score.
        """
        return max(
            (entry.score for entry in self._leaderboard.entries),
            default=0
        )

    def snapshot(self, score: int, max_rank: int = 10) -> int | None:
        """
        Return the rank a score would occupy in the leaderboard.

        Args:
            score: Score to record or compare.
            max_rank: Maximum leaderboard rank to include in the snapshot.

        Returns:
            The value produced by the snapshot operation.
        """
        rank = sum(entry.score >= score for entry in self._leaderboard.entries)
        if rank >= max_rank:
            return None
        return rank

    def save(self) -> bool:
        """
        Save the associated data.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
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
        """
        Load the associated data.
        """
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
        """
        Handle load leaderboard file.

        Returns:
            The value produced by the load leaderboard file operation.
        """
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
        """
        Handle generate empty leaderboard.

        Returns:
            The value produced by the generate empty leaderboard operation.
        """
        return LeaderboardModel()

    def get_secret(self) -> bytes:
        """
        Return the current secret.

        Returns:
            The current secret.
        """
        if self._secret is None:
            self._load_secret()

        if self._secret is None:
            self._secret = self.generate_secret()
            self._save_secret()

        return self._secret

    def _load_secret(self) -> None:
        """
        Handle load secret.
        """
        try:
            with open(self._secret_path(), 'r') as f:
                secret = f.read()
                if len(secret.strip()) > 0:
                    self._secret = secret.encode()

        except (OSError, RuntimeError):
            pass

    def _save_secret(self) -> None:
        """
        Handle save secret.
        """
        try:
            Path(self._path).parent.mkdir(parents=True, exist_ok=True)
            with open(self._secret_path(), 'w', encoding='UTF-8') as f:
                f.write(self.get_secret().decode())
        except (OSError, RuntimeError) as e:
            self._logger.warning(f'Cannot save leaderboard secret : {e!s}')

    def _secret_path(self) -> Path:
        """
        Return the path of the secret, stored next to the highscore file.

        Returns:
            The path of the secret file.
        """
        return Path(self._path).parent / SECRET_FILENAME

    def generate_secret(self) -> bytes:
        """
        Generate a cryptographic secret for the leaderboard.

        Returns:
            The value produced by the generate secret operation.
        """
        return secrets.token_hex(nbytes=16).encode('utf-8')

    def _hash_function(self, payload: bytes) -> str:
        """
        Handle hash function.

        Args:
            payload: Bytes to hash or encode.

        Returns:
            The value produced by the hash function operation.
        """
        return hmac.new(self.get_secret(), payload, hashlib.sha256).hexdigest()

    def _get_first_hash(self) -> str:
        """
        Handle get first hash.

        Returns:
            The value produced by the get first hash operation.
        """
        return self._hash_function(b'None|0|' + self.get_secret())

    def set_path(self, path: str) -> None:
        """
        Assign the path.

        Args:
            path: Filesystem path used to load or save the data.
        """
        normalized_path = str(Path(path).expanduser().resolve())
        self._path = normalized_path
