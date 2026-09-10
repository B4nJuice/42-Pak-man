from pydantic import BaseModel, Field


class ConfigModel(BaseModel):
    highscore_path: str = Field(
        'data/highscores.json', description='Path to the highscore file'
    )
