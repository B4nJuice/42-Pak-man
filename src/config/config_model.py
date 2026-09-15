from pydantic import BaseModel, Field


class ConfigModel(BaseModel):
    highscore_path: str = Field(
        'data/highscores.json', description='Path to the highscore file'
    )
    level_width: int = Field(
        20, description='Width of the level', lt=30
    )
    level_height: int = Field(
        20, description='Height of the level'
    )
