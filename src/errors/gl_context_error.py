from src.errors.base_error import BaseError


class GlContextError(BaseError):
    def __init__(self) -> None:
        super().__init__('Context not created')