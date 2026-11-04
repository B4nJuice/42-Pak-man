from pydantic import BaseModel, Field


class LevelModel(BaseModel):
    name: str = Field(
        default='unnamed level',
        description='name of the level'
    )
    seed: int = Field(
        default=1,
        description='Seed of the level'
    )
    level_width: int = Field(
        default=20,
        description='Width of the level'
    )
    level_height: int = Field(
        default=20,
        description='Height of the level'
    )
