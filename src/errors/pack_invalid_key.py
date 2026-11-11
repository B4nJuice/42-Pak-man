from src.errors.pack_error import PackError


class PackInvalidKey(PackError):
    def __init__(self, key: str) -> None:
        """
        Initialize the instance.

        Args:
            key: Keyboard key code associated with the action.
        """
        super().__init__(f'unknown texture entry {key!r}')
