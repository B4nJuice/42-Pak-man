from src.errors.pack_error import PackError


class PackInvalidKey(PackError):
    def __init__(self, key: str) -> None:
        super().__init__(f'unknown texture entry {key!r}')
