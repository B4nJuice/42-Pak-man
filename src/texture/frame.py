from pathlib import Path

from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class Frame:
    path: Path
    duration: float
