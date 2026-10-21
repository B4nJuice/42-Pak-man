from pathlib import Path

from src.errors.texture_pack_error import TexturePackError


class AssetLoadError(TexturePackError):
    def __init__(
        self,
        path: str | Path,
        *,
        pack: str | Path | None = None,
        reason: str | None = None,
    ) -> None:
        message = f'Unable to load asset {Path(path).as_posix()!r}'
        if reason:
            message = f'{message}: {reason}'
        super().__init__(message, pack=pack)
