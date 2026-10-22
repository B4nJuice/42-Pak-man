import hmac
import json
from collections.abc import Callable
from datetime import datetime

from pydantic import BaseModel, Field

from src.utils import utc_now


class LeaderboardEntryModel(BaseModel):
    name: str = Field(min_length=3, max_length=15)
    score: int = Field(ge=0)
    timestamp: datetime = Field(default_factory=utc_now)

    sig: str | None = Field(default=None)

    def compile(self, prevus_sig: str) -> str:
        self.sig = prevus_sig
        payload = self.model_dump_json()

        return payload


class LeaderboardModel(BaseModel):
    entries: list[LeaderboardEntryModel] = Field(default=[])
    sig: str | None = Field(default=None)

    def add(self, entry: LeaderboardEntryModel) -> bool:
        min_score: int = min((x.score for x in self.entries), default=0)
        leaderboard_is_full: bool = len(self.entries) >= 10

        self._sort()
        if leaderboard_is_full and entry.score <= min_score:
            return False

        if leaderboard_is_full:
            self.entries.pop()
        self.entries.append(entry)
        self._sort()

        return True

    def _sort(self) -> None:
        self.entries.sort(
            key=lambda x: (-x.score, x.timestamp)
        )

    def verify(
                self,
                hash_func: Callable[[bytes], str],
                first_hash: str
            ) -> bool:
        if self.sig is None:
            return False

        compiled = self.compile(hash_func, first_hash)
        return hmac.compare_digest(compiled, self.sig)

    def clean(self) -> None:
        self.sig = None

    def clear(self) -> None:
        self.entries = []
        self.clean()

    def compile(
                self,
                hash_func: Callable[[bytes], str],
                first_hash: str
            ) -> str:
        entries: list[str] = []
        last_hash: str = first_hash

        for index, entry in enumerate(self.entries):
            str_entry: str = entry.compile(last_hash)
            entries.append(str_entry)
            last_hash = hash_func(
                last_hash.encode()
                + b'|' + str(index).encode()
                + b'|' + str_entry.encode()
            )

        return hash_func(json.dumps(entries).encode())
