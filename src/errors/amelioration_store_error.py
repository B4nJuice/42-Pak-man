from src.errors.base_error import BaseError


class AmeliorationStoreNotFound(BaseError):
    def __init__(self, cls: str) -> None:
        """
        Initialize the instance.
        """
        super().__init__(f'Amelioration: {cls} not initialized')
