from src.errors.base_error import BaseError


class EntityStoreNotFound(BaseError):
    def __init__(self, cls: str) -> None:
        super().__init__(f'EntityStore: {cls} not initialized')
