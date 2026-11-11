from src.errors.base_error import BaseError


class SkillStoreNotFound(BaseError):
    def __init__(self, cls: str) -> None:
        """
        Initialize the instance.
        """
        super().__init__(f'Skill: {cls} not initialized')
