from pathlib import Path

from src.errors.pack_error import PackError


class TexturePackError(PackError):
    def __init__(
        self,
        message: str,
        *,
        pack: str | Path | None = None,
        key: str | None = None,
        value: object | None = None,
    ) -> None:
        """
        Initialize the instance.

        Args:
            message: Message to write to the log or display.
            pack: Pack used by the operation.
            key: Keyboard key code associated with the action.
            value: Value to assign or apply.
        """
        details: list[str] = []
        if pack is not None:
            details.append(f'pack={str(pack)!r}')
        if key is not None:
            details.append(f'key={key!r}')
        if value is not None:
            details.append(f'value={value!r}')
        suffix = f' ({", ".join(details)})' if details else ''
        super().__init__(f'{message}{suffix}')
