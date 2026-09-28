from pydantic import BaseModel, Field


class ConfigModel(BaseModel):
    highscore_path: str = Field(
        default='data/highscores.json',
        description='Path to the highscore file'
    )
    level_width: int = Field(
        default=20,
        description='Width of the level'
    )
    level_height: int = Field(
        default=20,
        description='Height of the level'
    )

    screen_width: int = Field(
        gt=100,
        default=800,
        description='Width of the screen'
    )
    screen_height: int = Field(
        gt=100,
        default=600,
        description='Height of the screen'
    )
