from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Frame:
    path: Path
    duration: float
