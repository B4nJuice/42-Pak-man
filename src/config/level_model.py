from pydantic import BaseModel, Field

FIRST_LEVEL_SEED: int = 42
MIN_LEVEL_SIZE: int = 5
MAX_LEVEL_SIZE: int = 100


class LevelModel(BaseModel):
    name: str = Field(
        default='unnamed level',
        description='name of the level'
    )
    seed: int | None = Field(
        default=None,
        ge=0,
        description=(
            'Seed of the level. When omitted, the first level uses '
            f'{FIRST_LEVEL_SEED} and the following levels are random.'
        )
    )
    level_width: int = Field(
        default=20,
        ge=MIN_LEVEL_SIZE,
        le=MAX_LEVEL_SIZE,
        description='Width of the level'
    )
    level_height: int = Field(
        default=20,
        ge=MIN_LEVEL_SIZE,
        le=MAX_LEVEL_SIZE,
        description='Height of the level'
    )
    max_time: int = Field(
        default=90,
        gt=0,
        description='Max time to finish the level, in seconds'
    )
